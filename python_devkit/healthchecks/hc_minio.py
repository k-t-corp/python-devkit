import time
import requests


def hc_minio(uri: str, client_timeout: int, retries: int, retry_interval_seconds: int):
    retries_left = retries
    while retries_left > 0:
        try:
            requests.get(uri, timeout=client_timeout)
            print(f"Established minio connection on uri={uri}")
            return
        except Exception as e:
            print(f"Failed healthcheck on minio uri={uri}, "
                  f"{retries_left} retries left, "
                  f"retrying in {retry_interval_seconds} seconds")
        time.sleep(retry_interval_seconds)
        retries_left -= 1
