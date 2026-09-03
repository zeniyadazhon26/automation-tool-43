import time
from functools import wraps
from collections import defaultdict
import heapq

class CostAdaptiveCache:
    def __init__(self, max_size=1000, eviction_ratio=0.2):
        self.max_size = max_size
        self.eviction_ratio = eviction_ratio
        self.cache = {}
        self.benefit_heap = []
        self.stats = defaultdict(lambda: {"hits": 0, "compute_time": 0.0, "lookup_time": 0.0})

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, tuple(sorted(kwargs.items())))
            
            t0 = time.perf_counter()
            if key in self.cache:
                result = self.cache[key]
                t1 = time.perf_counter()
                self.stats[key]["hits"] += 1
                self.stats[key]["lookup_time"] += (t1 - t0)
                return result
            
            t0 = time.perf_counter()
            result = func(*args, **kwargs)
            t1 = time.perf_counter()
            
            compute_duration = t1 - t0
            
            if compute_duration > 1e-6:
                if len(self.cache) >= self.max_size:
                    self._evict()
                self.cache[key] = result
                benefit = compute_duration
                heapq.heappush(self.benefit_heap, (benefit, key))
                
            return result
        return wrapper

    def _evict(self):
        num_to_evict = max(1, int(self.max_size * self.eviction_ratio))
        temp_heap = []
        for benefit, key in self.benefit_heap:
            if key not in self.cache:
                continue
            stats = self.stats[key]
            real_benefit = (stats["hits"] + 1) * benefit - stats["lookup_time"]
            heapq.heappush(temp_heap, (real_benefit, key))
        
        self.benefit_heap = temp_heap
        for _ in range(num_to_evict):
            if not self.benefit_heap:
                break
            _, key = heapq.heappop(self.benefit_heap)
            self.cache.pop(key, None)
            self.stats.pop(key, None)

adaptive_cache = CostAdaptiveCache(max_size=100)

@adaptive_cache
def expensive_transform(data_vector: tuple) -> float:
    total = sum(x ** 1.5 for x in data_vector)
    if int(total) % 7 == 0:
        time.sleep(0.002)
    return total