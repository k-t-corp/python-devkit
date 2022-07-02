import os
import yaml
import shutil
from string import Template


def write_production_files(cwd: str, uwsgi_module: str, uwsgi_callable: str):
    # write docker-compose.prod.yml
    docker_compose = {
        "version": "3.9",
        "services": {
            "web": {
                "image": "app",
                "entrypoint": "sh -c \"python wait.py && uwsgi --ini uwsgi.ini\"",
                "env_file": [
                    "$HOME/env"
                ],
                "restart": "always",
                "network_mode": "host"
            },
            "clock": {
                "image": "app",
                "entrypoint": "sh -c \"python wait.py && python cli.py start_clock\"",
                "env_file": [
                    "$HOME/env"
                ],
                "restart": "always",
                "network_mode": "host"
            },
            "worker": {
                "image": "app",
                "entrypoint": "sh -c \"python wait.py && python cli.py start_worker\"",
                "env_file": [
                    "$HOME/env"
                ],
                "restart": "always",
                "network_mode": "host"
            },
            "db-migration": {
                "image": "app",
                "entrypoint": "sh -c \"python wait.py && python cli.py start_database_migration\"",
                "env_file": [
                    "$HOME/env"
                ],
                "network_mode": "host",
                "profiles": [
                    "one-off"
                ]
            }
        }
    }

    docker_compose_dir = os.path.join(cwd, "docker-compose.prod.yml")
    with open(docker_compose_dir, "w") as f:
        yaml.dump(docker_compose, f, default_flow_style=False, indent=2, sort_keys=False)

    # write production.Dockerfile
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

    template_dockerfile_dir = os.path.join(templates_dir, "production.Dockerfile")
    dockerfile_dir = os.path.join(cwd, "Dockerfile")
    shutil.copyfile(template_dockerfile_dir, dockerfile_dir)

    # write stop.sh
    template_stop_sh_dir = os.path.join(templates_dir, "stop.sh")
    stop_sh_dir = os.path.join(cwd, "stop.sh")
    shutil.copyfile(template_stop_sh_dir, stop_sh_dir)

    # write start.sh
    template_start_sh_dir = os.path.join(templates_dir, "start.sh")
    start_sh_dir = os.path.join(cwd, "start.sh")
    shutil.copyfile(template_start_sh_dir, start_sh_dir)

    # write uwsgi.ini
    template_uwsgi_ini_dir = os.path.join(templates_dir, "uwsgi.ini")
    with open(template_uwsgi_ini_dir, 'r') as f:
        uwsgi_ini = Template(f.read()).substitute(
            module=uwsgi_module,
            callable=uwsgi_callable
        )
    uwsgi_ini_dir = os.path.join(cwd, "uwsgi.ini")
    with open(uwsgi_ini_dir, 'w') as f:
        f.write(uwsgi_ini)

    # write wait.py
    template_wait_py_dir = os.path.join(templates_dir, "wait.py")
    wait_py_dir = os.path.join(cwd, "wait.py")
    shutil.copyfile(template_wait_py_dir, wait_py_dir)
