import time
import random
from functools import wraps

class NetworkException(Exception):
    pass

class TransientNetworkException(NetworkException):
    pass

class FatalNetworkException(NetworkException):
    pass

def retry_on_network_error(max_retries=3, initial_delay=1.0, backoff_factor=2, max_delay=30.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except FatalNetworkException as e:
                    raise
                except TransientNetworkException as e:
                    if attempt == max_retries:
                        raise NetworkException(f"Max retries ({max_retries}) exceeded for network op") from e
                    jitter = random.uniform(0, delay * 0.1)
                    sleep_duration = min(delay + jitter, max_delay)
                    time.sleep(sleep_duration)
                    delay *= backoff_factor
                except Exception as e:
                    if attempt == max_retries:
                        raise NetworkException(f"Max retries exceeded: {str(e)}") from e
                    jitter = random.uniform(0, delay * 0.1)
                    sleep_duration = min(delay + jitter, max_delay)
                    time.sleep(sleep_duration)
                    delay *= backoff_factor
            raise NetworkException("Unexpected end of retry logic")
        return wrapper
    return decorator

def simulate_network_call(success_after=2):
    if not hasattr(simulate_network_call, 'attempt_count'):
        simulate_network_call.attempt_count = 0
    simulate_network_call.attempt_count += 1
    if simulate_network_call.attempt_count <= success_after:
        if simulate_network_call.attempt_count % 2 == 0:
            raise TransientNetworkException("Temporary connection lost")
        else:
            raise Exception("General network glitch")
    return {"status": "connected", "data": "retrieved"}

if __name__ == "__main__":
    @retry_on_network_error(max_retries=4, initial_delay=0.1, backoff_factor=1.5, max_delay=1.0)
    def test_network():
        return simulate_network_call(success_after=2)
    result = test_network()
    print(result)