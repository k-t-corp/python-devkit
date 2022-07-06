import os
import yaml
from typing import List
from .services import service_to_composes


def write_development_files(cwd: str, services: List[str]):
    docker_compose_services = {}
    for service in services:
        if service in service_to_composes:
            docker_compose_services.update(service_to_composes[service])
        else:
            print(f"Cannot find compose for service {service}")

    docker_compose = {
        "version": "3.9",
        "services": docker_compose_services
    }

    docker_compose_dir = os.path.join(cwd, "docker-compose.yml")
    with open(docker_compose_dir, "w") as f:
        yaml.dump(docker_compose, f, default_flow_style=False, indent=2, sort_keys=False)
