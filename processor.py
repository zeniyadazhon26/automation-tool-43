import collections
import functools
from typing import Any, Callable, Dict, List, Union

class DataTransformer:
    def __init__(self, data: Any):
        self.data = data

    def pipeline(self, *funcs: Callable[[Any], Any]) -> 'DataTransformer':
        self.data = functools.reduce(lambda acc, f: f(acc), funcs, self.data)
        return self

def flatten_dict(d: Dict, parent_key: str = '', sep: str = '_') -> Dict:
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def scrub_nulls(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: scrub_nulls(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [scrub_nulls(x) for x in obj if x is not None]
    return obj

def batch_process(items: List[Any], chunk_size: int = 5) -> List[List[Any]]:
    it = iter(items)
    return list(iter(lambda: list(collections.islice(it, chunk_size)), []))

def deep_transform(data: Any, transformer: Callable[[Any], Any]) -> Any:
    if isinstance(data, dict):
        return {k: deep_transform(v, transformer) for k, v in data.items()}
    if isinstance(data, list):
        return [deep_transform(v, transformer) for v in data]
    return transformer(data)