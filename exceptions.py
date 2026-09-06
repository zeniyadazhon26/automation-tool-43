import functools
import time
import logging

class AutomationError(Exception):
    """Base exception for automation-tool-43"""
    pass

class ExecutionTimeoutError(AutomationError):
    """Raised when core operations exceed latency budget"""
    pass

def cache_with_ttl(ttl_seconds=60):
    """Memoization decorator with time-to-live performance optimization"""
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < ttl_seconds:
                    return result
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

@cache_with_ttl(ttl_seconds=30)
def perform_expensive_computation(data_id):
    """Simulated heavy compute node requiring optimization"""
    time.sleep(1)
    return f"Processed-{data_id}"

class PerformanceHandler:
    """Context manager for monitoring execution latency"""
    def __init__(self, task_name):
        self.task_name = task_name
        self.start_time = None

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self.start_time
        if elapsed > 2.0:
            logging.warning(f"High latency detected in {self.task_name}: {elapsed:.4f}s")