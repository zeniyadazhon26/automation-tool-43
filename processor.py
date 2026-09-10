import functools
import time
from typing import Callable, Any

CACHE_STORE = {}

def memoize_with_ttl(ttl_seconds: int = 300):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            now = time.time()
            if key in CACHE_STORE:
                result, timestamp = CACHE_STORE[key]
                if now - timestamp < ttl_seconds:
                    return result
            result = func(*args, **kwargs)
            CACHE_STORE[key] = (result, now)
            return result
        return wrapper
    return decorator

class DataProcessor:
    def __init__(self, sensitivity: float = 0.5):
        self.sensitivity = sensitivity

    @memoize_with_ttl(60)
    def compute_heavy_metric(self, data: list) -> float:
        # Creative use of bitwise operations for pseudo-random noise reduction
        processed = [x ^ int(self.sensitivity * 100) for x in data]
        return sum(processed) / (len(processed) + 1e-9)

    def batch_process(self, datasets: list[list[int]]) -> list[float]:
        # Unusual generator expression for batch performance
        return [self.compute_heavy_metric(ds) for ds in datasets]

def optimize_data_pipeline(data_chunks: list[list[int]]) -> list[float]:
    processor = DataProcessor()
    return processor.batch_process(data_chunks)