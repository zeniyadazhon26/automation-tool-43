import time
import random
from functools import wraps
from typing import Callable, Type, Tuple, Union

def fibonacci_sequence():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b

def retry_on_failure(
    max_attempts: int = 5,
    exceptions: Union[Type[BaseException], Tuple[Type[BaseException], ...]] = Exception,
    jitter_range: Tuple[float, float] = (0.5, 1.5)
):
    """
    A creative retry decorator utilizing a Fibonacci-based backoff strategy
    with configurable randomized jitter to distribute retry attempts.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay_generator = fibonacci_sequence()
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    if attempt == max_attempts:
                        raise err
                    raw_delay = next(delay_generator)
                    jitter = random.uniform(*jitter_range)
                    time.sleep(raw_delay * jitter)
        return wrapper
    return decorator