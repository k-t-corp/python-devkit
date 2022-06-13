import shutil
import os
import json
import yaml
import subprocess
import sys
import dotenv
from typing import Optional, List
from python_devkit.healthchecks import healthcheck_mongodb, healthcheck_redis, healthcheck_minio
from python_devkit.services import mongodb, redis, minio

if not shutil.which("docker-compose"):
    raise RuntimeError("docker-compose is not found on PATH, exiting")
DOCKER_COMPOSE = shutil.which("docker-compose")

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
        if not run([DOCKER_COMPOSE, "down"], locking_dir):
            raise RuntimeError()

    # overwrite docker-compose.yml for this stack
    cwd = os.getcwd()
    python_devkit_dir = os.path.join(cwd, ".python-devkit.json")
    if not os.path.exists(python_devkit_dir):
        print(f".python-devkit.json file {python_devkit_dir} not found")
        raise RuntimeError()
    with open(python_devkit_dir) as f:
        services = json.load(f)["services"]

    docker_compose_services = {}
    for service in services:
        if service == "mongodb":
            docker_compose_services.update(mongodb())
        if service == "redis":
            docker_compose_services.update(redis())
        if service == "minio":
            docker_compose_services.update(minio())

    docker_compose = {
        "version": "3.9",
        "services": docker_compose_services
    }

    docker_compose_dir = os.path.join(cwd, "docker-compose.yml")
    with open(docker_compose_dir, "w") as f:
        yaml.dump(docker_compose, f, default_flow_style=False, indent=2, sort_keys=False)

    # start this stack
    lock_with_cwd()

    if not run([DOCKER_COMPOSE, "up", "-d"], cwd):
        raise RuntimeError()

    # wait for stack to be fully healthy
    for service in services:
        if service == "mongodb":
            healthcheck_mongodb()
        if service == "redis":
            healthcheck_redis()
        if service == "minio":
            healthcheck_minio()

    try:
        # export env and run Procfile
        dotenv.load_dotenv(os.path.join(cwd, ".env"))
        run([HEROKU, "local", "-f", "Procfile.dev"], cwd)
    except KeyboardInterrupt:
        print("Stopping stack")

        # stop this stack
        run([DOCKER_COMPOSE, "down"], cwd)
        unlock_with_cwd()


if __name__ == '__main__':
    main()
