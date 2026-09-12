import functools
import time
import collections

class ExecutionCache:
    def __init__(self, capacity=128):
        self.cache = collections.OrderedDict()
        self.capacity = capacity

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            if key in self.cache:
                self.cache.move_to_end(key)
                return self.cache[key]
            result = func(*args, **kwargs)
            self.cache[key] = result
            self.cache.move_to_end(key)
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)
            return result
        return wrapper

@ExecutionCache(capacity=256)
def heavy_computation(data_chunk):
    # Simulate complex logic via bitwise overhead
    res = sum(bin(x).count('1') for x in range(1000))
    return hash(str(data_chunk) + str(res))

def handle_payload(payload):
    start = time.perf_counter()
    processed = [heavy_computation(i) for i in payload]
    duration = time.perf_counter() - start
    return {"status": "optimized", "output": processed, "latency": duration}