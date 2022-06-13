import time
import pymongo
import redis
import requests

RETRIES = 6
RETRY_INTERVAL_SECONDS = 5

MONGO_PORT = 19023
MONGO_CLIENT_TIMEOUT_MS = 1000  # 1 second

REDIS_PORT = 19024
REDIS_CLIENT_TIMEOUT = 1000  # 1 second

MINIO_PORT = 19025
MINIO_CLIENT_TIMEOUT = 1  # 1 second


def healthcheck_mongodb():
    uri = f"mongodb://localhost:{MONGO_PORT}"
    c = pymongo.MongoClient(uri, serverSelectionTimeoutMS=MONGO_CLIENT_TIMEOUT_MS)

    retries = RETRIES
    while retries > 0:
        try:
            c.server_info()
            print(f"Established MongoDB connection on {uri}")
            return
        except:
            print(f"Failed healthcheck on MongoDB {uri}, "
                  f"{retries} retries left, "
                  f"retrying in {RETRY_INTERVAL_SECONDS} seconds")
        time.sleep(RETRY_INTERVAL_SECONDS)
        retries -= 1


def healthcheck_redis():
    host, port = "localhost", REDIS_PORT
    r = redis.Redis(host=host, port=port, socket_connect_timeout=REDIS_CLIENT_TIMEOUT)

    retries = RETRIES
    while retries > 0:
        try:
            r.ping()
            print(f"Established Redis connection on host={host} port={port}")
            return
        except:
            print(f"Failed healthcheck on Redis host={host} port={port}, "
                  f"{retries} retries left, "
                  f"retrying in {RETRY_INTERVAL_SECONDS} seconds")
        time.sleep(RETRY_INTERVAL_SECONDS)
        retries -= 1


def healthcheck_minio():
    uri = f"http://localhost:{MINIO_PORT}"

    retries = RETRIES
    while retries > 0:
        try:
            requests.get(uri, timeout=MINIO_CLIENT_TIMEOUT)
            print(f"Established Redis connection on {uri}")
            return
        except:
            print(f"Failed healthcheck on Minio {uri}, "
                  f"{retries} retries left, "
                  f"retrying in {RETRY_INTERVAL_SECONDS} seconds")
        time.sleep(RETRY_INTERVAL_SECONDS)
        retries -= 1
