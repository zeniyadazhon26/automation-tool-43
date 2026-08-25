import time
import random

def fibonacci_delay(attempt):
    if attempt <= 1:
        return 1
    a, b = 1, 1
    for _ in range(2, attempt):
        a, b = b, a + b
    return b

class NetworkHandler:
    def __init__(self, max_retries=3, base_delay=1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay

    def execute(self, network_func):
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return network_func()
            except Exception as error:
                last_error = error
                if attempt == self.max_retries:
                    break
                delay = fibonacci_delay(attempt) * self.base_delay + random.uniform(0, 0.5)
                time.sleep(delay)
        raise ConnectionError(f"Network operation failed after {self.max_retries} retries") from last_error

def example_network_operation():
    if random.random() > 0.4:
        raise TimeoutError("Simulated network timeout")
    return "Successfully fetched network data"

if __name__ == "__main__":
    handler = NetworkHandler(max_retries=4, base_delay=0.5)
    try:
        result = handler.execute(example_network_operation)
        print("Result:", result)
    except ConnectionError as e:
        print("Error:", str(e))