from python_devkit.healthchecks import hc_mongodb, hc_redis, hc_minio
from .services import MONGO_URI, REDIS_HOST, REDIS_PORT, MINIO_URI

RETRIES = 6
RETRY_INTERVAL_SECONDS = 5

MONGO_CLIENT_TIMEOUT_MS = 1000  # 1 second
REDIS_CLIENT_TIMEOUT = 1000  # 1 second
MINIO_CLIENT_TIMEOUT = 1  # 1 second


def mongodb():
    hc_mongodb(MONGO_URI, MONGO_CLIENT_TIMEOUT_MS, RETRIES, RETRY_INTERVAL_SECONDS)


def redis():
    hc_redis(REDIS_HOST, REDIS_PORT, REDIS_CLIENT_TIMEOUT, RETRIES, RETRY_INTERVAL_SECONDS)


def minio():
    hc_minio(MINIO_URI, MINIO_CLIENT_TIMEOUT, RETRIES, RETRY_INTERVAL_SECONDS)


service_to_healthchecks = {
    "mongodb": mongodb,
    "redis": redis,
    "minio": minio
}
