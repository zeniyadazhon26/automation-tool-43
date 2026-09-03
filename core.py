import collections
from typing import Callable, Any, Generator

class FastTask:
    __slots__ = ('func', 'args', 'kwargs', 'task_id')

    def __init__(self, func: Callable, *args: Any, **kwargs: Any):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.task_id = self._generate_id(args, kwargs)

    def _generate_id(self, args: tuple, kwargs: dict) -> int:
        h = 14695981039346656037
        for val in args:
            h = (h ^ hash(val)) * 1099511628211 & 0xffffffffffffffff
        for k, v in sorted(kwargs.items()):
            h = (h ^ hash(k) ^ hash(v)) * 1099511628211 & 0xffffffffffffffff
        return h

class CoreEngine:
    def __init__(self, capacity: int = 2048):
        self.tasks = collections.deque()
        self.cache = {}
        self.capacity = capacity

    def queue_task(self, func: Callable, *args: Any, **kwargs: Any) -> None:
        self.tasks.append(FastTask(func, *args, **kwargs))

    def execute_pipeline(self) -> Generator[Any, None, None]:
        while self.tasks:
            task = self.tasks.popleft()
            tid = task.task_id
            if tid in self.cache:
                yield self.cache[tid]
            else:
                res = task.func(*task.args, **task.kwargs)
                if len(self.cache) >= self.capacity:
                    oldest_key = next(iter(self.cache))
                    self.cache.pop(oldest_key)
                self.cache[tid] = res
                yield res
