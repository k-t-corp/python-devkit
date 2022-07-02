import os
import yaml
from typing import List
from python_devkit.healthchecks import MONGO_PORT, REDIS_PORT, MINIO_PORT


def mongodb():
    return {
        "mongodb": {
            "image": "mongo:4.4",
            "volumes": [
                "${PWD}/data/mongodb_data:/data/db"
            ],
            "ports": [
                f"{MONGO_PORT}:27017"
            ],
            "healthcheck": {
                "test": "echo 'db.runCommand(\"ping\").ok' | mongo localhost:27017/test --quiet",
                "interval": "10s",
                "timeout": "10s",
                "retries": 10
            }
        }
    }


def redis():
    return {
        "redis": {
            "image": "redis",
            "volumes": [
                "${PWD}/data/redis_data:/data"
            ],
            "ports": [
                f"{REDIS_PORT}:6379"
            ],
            "healthcheck": {
                "test": [
                    "CMD",
                    "redis-cli",
                    "ping"
                ],
                "interval": "1s",
                "timeout": "3s",
                "retries": 30
            }
        }
    }


def minio():
    return {
        "minio": {
            "image": "minio/minio:RELEASE.2021-06-09T18-51-39Z",
            "command": [
                "server",
                "/data"
            ],
            "volumes": [
                "${PWD}/data/minio_data:/data"
            ],
            "ports": [
                f"{MINIO_PORT}:9000"
            ],
            "environment": {
                "MINIO_ROOT_USER": "minioadmin",
                "MINIO_ROOT_PASSWORD": "minioadmin"
            },
            "healthcheck": {
                "test": [
                    "CMD",
                    "curl",
                    "-f",
                    "http://localhost:9000/minio/health/live"
                ],
                "interval": "30s",
                "timeout": "20s",
                "retries": 3
            }
        }
    }


def write_development_files(cwd: str, services: List[str]):
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
