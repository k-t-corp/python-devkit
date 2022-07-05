import time
import pymongo


def hc_mongodb(uri: str, client_timeout_ms: int, retries: int, retry_interval_seconds: int):
    c = pymongo.MongoClient(uri, serverSelectionTimeoutMS=client_timeout_ms)

    retries_left = retries
    while retries_left > 0:
        try:
            c.server_info()
            print(f"Established MongoDB connection on {uri}")
            return
        except Exception as e:
            print(f"Failed healthcheck on MongoDB {uri}, "
                  f"{retries_left} retries left, "
                  f"retrying in {retry_interval_seconds} seconds")
        time.sleep(retry_interval_seconds)
        retries_left -= 1
