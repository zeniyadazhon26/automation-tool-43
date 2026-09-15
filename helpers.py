from typing import Any, Callable, Dict, List, Optional
import functools

def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Chain multiple functions together like a pipeline."""
    def pipeline(data: Any) -> Any:
        return functools.reduce(lambda v, f: f(v), functions, data)
    return pipeline

def deep_update(mapping: Dict[Any, Any], *updating_maps: Dict[Any, Any]) -> Dict[Any, Any]:
    """Recursively merge dictionary structures with style."""
    updated = mapping.copy()
    for update in updating_maps:
        for key, value in update.items():
            if isinstance(value, dict) and key in updated and isinstance(updated[key], dict):
                updated[key] = deep_update(updated[key], value)
            else:
                updated[key] = value
    return updated

def retry_on_failure(attempts: int = 3) -> Callable[[Callable], Callable]:
    """Decorator for resilient execution of unstable tasks."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex: Optional[Exception] = None
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
            raise last_ex if last_ex else RuntimeError("failed")
        return wrapper
    return decorator