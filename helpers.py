import time
import functools
import random
from typing import Callable, Any

def retry_with_jitter(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception:
                    attempts += 1
                    if attempts == max_attempts:
                        raise
                    time.sleep(base_delay * (2 ** attempts) + random.uniform(0, 0.1))
        return wrapper
    return decorator

def batch_process(iterable: list, size: int):
    """Generator yielding chunks of the input list."""
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

def singleton(cls):
    """Decorator for classes with single instance."""
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

def silent_executor(func: Callable, default: Any = None):
    """Wraps execution to ignore all exceptions."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return default
    return wrapper