import shutil
import os
import json
import subprocess
import sys
import dotenv
from typing import Optional, List
from python_devkit.dev.healthchecks import service_to_healthchecks
from python_devkit.dev.write_files import write_development_files
from python_devkit.production import write_production_files

if not shutil.which("docker-compose"):
    print("docker-compose is not found on PATH, trying to find docker")
    if not shutil.which("docker"):
        raise RuntimeError("docker is not found on PATH, exiting")
    DOCKER_COMPOSE = [shutil.which("docker"), "compose"]
else:
    DOCKER_COMPOSE = [shutil.which("docker-compose")]

if not shutil.which("heroku"):
    raise RuntimeError("heroku is not found on PATH, exiting")
HEROKU = shutil.which("heroku")


cli_dir = os.path.join(os.path.expanduser("~"), ".python-devkit")

if not os.path.exists(cli_dir):
    print(f"Creating directory for python-devkit {cli_dir}")
    os.mkdir(cli_dir)

locking_dir_dir = os.path.join(cli_dir, "locking-dir.json")


def get_locking_dir() -> Optional[str]:
    if not os.path.exists(locking_dir_dir):
        return None
    with open(locking_dir_dir) as f:
        locking_dir = json.load(f)["dir"]
        if not os.path.exists(locking_dir):
            print(f"Locking directory last time was {locking_dir} but it no longer exists. "
                  f"You may need to manually clean up resources on the moved directory "
                  f"before proceeding with any operation.")
            return None
        return locking_dir


def lock_with_cwd():
    locking_dir = os.getcwd()
    with open(locking_dir_dir, 'w') as f:
        json.dump({
            "dir": locking_dir
        }, f)


def unlock_with_cwd():
    os.remove(locking_dir_dir)


def run(command: List[str], cwd: str) -> bool:
    p = subprocess.Popen(command, cwd=cwd, stdout=sys.stdout, stderr=sys.stdout)
    p.communicate()
    ret = p.returncode
    if ret != 0:
        print(f"Failed to run command \"{' '.join(command)}\" on directory {cwd}")
    return ret == 0


def main():
    # find existing stacks and stop
    locking_dir = get_locking_dir()
    if locking_dir:
        print(f"Bringing down existing stack on directory {locking_dir}")
        if not run(DOCKER_COMPOSE + ["down"], locking_dir):
            raise RuntimeError()
    cwd = os.getcwd()

    # parse configuration file
    python_devkit_dir = os.path.join(cwd, ".python-devkit.json")
    if not os.path.exists(python_devkit_dir):
        print(f".python-devkit.json file {python_devkit_dir} not found")
        raise RuntimeError()
    with open(python_devkit_dir) as f:
        config = json.load(f)
        dev_services = config["dev"]["services"]
        production_uwsgi_module = config["production"]["app"]["web"]["uwsgi_module"]
        production_uwsgi_callable = config["production"]["app"]["web"]["uwsgi_callable"]

    # write development docker-compose.yml
    write_development_files(cwd, dev_services)

    # write production files
    write_production_files(cwd, production_uwsgi_module, production_uwsgi_callable)

    # start development stack
    lock_with_cwd()

    if not run(DOCKER_COMPOSE + ["up", "-d"], cwd):
        raise RuntimeError()

    # wait for stack to be fully healthy
    for dev_service in dev_services:
        if dev_service in service_to_healthchecks:
            service_to_healthchecks[dev_service]()
        else:
            print(f"Cannot find healthcheck for service {dev_service}")

    try:
        # export env and run Procfile
        dotenv.load_dotenv(os.path.join(cwd, ".env"))
        run([HEROKU, "local", "-f", "Procfile.dev"], cwd)
    except KeyboardInterrupt:
        print("Stopping stack")

        # stop this stack
        run(DOCKER_COMPOSE + ["down"], cwd)
        unlock_with_cwd()


if __name__ == '__main__':
    main()
