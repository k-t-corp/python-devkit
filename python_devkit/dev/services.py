MONGO_PORT = 19023
MONGO_URI = f"mongodb://localhost:{MONGO_PORT}"

REDIS_HOST = "localhost"
REDIS_PORT = 19024

MINIO_PORT = 19025
MINIO_URI = f"http://localhost:{MINIO_PORT}"


MONGODB = {
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


REDIS = {
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


MINIO = {
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

service_to_composes = {
    "mongodb": MONGODB,
    "redis": REDIS,
    "minio": MINIO
}
