import os
import yaml


def write_production_files(cwd: str):
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

    # write Dockerfile

    # write stop.sh

    # write start.sh

    # write uwsgi.ini

    # write wait.py
    pass
