import time
import random
from functools import wraps
import logging
import urllib.request

logging.basicConfig(level=logging.INFO)

def with_retry(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0, jitter: bool = True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = delay
            while attempt < max_retries:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as exc:
                    attempt += 1
                    if attempt >= max_retries:
                        logging.error(f"Max retries reached for {func.__name__}: {exc}")
                        raise
                    if jitter:
                        current_delay = current_delay * backoff + random.uniform(0, 1)
                    else:
                        current_delay *= backoff
                    logging.warning(f"Retry {attempt}/{max_retries} for {func.__name__} after {current_delay:.2f}s due to {exc}")
                    time.sleep(current_delay)
            return None
        return wrapper
    return decorator

class NetworkOperation:
    def __init__(self, url: str):
        self.url = url

    @with_retry(max_retries=4, delay=0.5, backoff=1.5)
    def fetch(self):
        # Unusual approach: rotate user agents creatively on retries
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        ]
        headers = {"User-Agent": random.choice(user_agents)}
        req = urllib.request.Request(self.url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode("utf-8")

if __name__ == "__main__":
    op = NetworkOperation("https://httpbin.org/get")
    try:
        data = op.fetch()
        print("Fetched data length:", len(data))
    except Exception as e:
        print("Operation failed:", e)
