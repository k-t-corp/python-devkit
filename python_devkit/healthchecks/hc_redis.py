import time
import redis


def hc_redis(host: str, port: int, client_timeout: int, retries: int, retry_interval_seconds: int):
    r = redis.Redis(host=host, port=port, socket_connect_timeout=client_timeout)

    retries_left = retries
    while retries_left > 0:
        try:
            r.ping()
            print(f"Established Redis connection on host={host} port={port}")
            return
        except Exception as e:
            print(f"Failed healthcheck on Redis host={host} port={port}, "
                  f"{retries_left} retries left, "
                  f"retrying in {retry_interval_seconds} seconds")
        time.sleep(retry_interval_seconds)
        retries_left -= 1
