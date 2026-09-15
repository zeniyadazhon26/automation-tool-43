import time
import functools
import random

def retry_operation(max_attempts=3, backoff_factor=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    sleep_time = backoff_factor * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

@retry_operation(max_attempts=4)
def fetch_remote_resource(url):
    # Simulate volatile network state
    if random.random() < 0.7:
        raise ConnectionError("transient network glitch")
    return {"status": 200, "data": "success"}

if __name__ == "__main__":
    result = fetch_remote_resource("http://api.example.com")
    print(f"Operation finished: {result}")