import functools
import re
from typing import Any, Callable, Dict, List, Union


class Pipeable:
    """Wraps a helper function to allow bitwise OR pipe syntax (data | helper)."""

    def __init__(self, func: Callable):
        self.func = func
        functools.update_wrapper(self, func)

    def __ror__(self, other: Any) -> Any:
        return self.func(other)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.func(*args, **kwargs)


@Pipeable
def sanitize_keys(data: Union[Dict, List]) -> Union[Dict, List]:
    """Recursively convert dictionary keys to clean snake_case format."""
    if isinstance(data, list):
        return [sanitize_keys(item) for item in data]
    if not isinstance(data, dict):
        return data

    sanitized = {}
    for key, value in data.items():
        snake_key = re.sub(r"(?<!^)(?=[A-Z])", "_", str(key)).lower().replace("-", "_")
        sanitized[snake_key] = sanitize_keys(value)
    return sanitized


@Pipeable
def flatten_dict(data: Dict[str, Any], sep: str = ".") -> Dict[str, Any]:
    """Flatten a nested dictionary into key paths using generator iteration."""

    def _flatten(obj: Any, prefix: str = "") -> Any:
        if isinstance(obj, dict) and obj:
            for k, v in obj.items():
                new_prefix = f"{prefix}{sep}{k}" if prefix else str(k)
                yield from _flatten(v, new_prefix)
        else:
            yield (prefix, obj)

    return dict(_flatten(data))


def batch_process(items: List[Any], batch_size: int = 10) -> List[List[Any]]:
    """Split an iterable collection into structured chunks."""
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")
    return [items[i : i + batch_size] for i in range(0, len(items), batch_size)]


def coalesce(*args: Any, default: Any = None) -> Any:
    """Return first non-None value from arguments or specified default."""
    return next((arg for arg in args if arg is not None), default)
