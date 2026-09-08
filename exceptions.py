import logging
import functools

class AutomationError(Exception):
    """Base exception for automation-tool-43"""
    pass

class EdgeCaseRegistry:
    _faults = {}

    @classmethod
    def register(cls, exc_type):
        def decorator(func):
            cls._faults[exc_type] = func
            return func
        return decorator

    @classmethod
    def resolve(cls, exc):
        handler = cls._faults.get(type(exc))
        return handler(exc) if handler else None

@EdgeCaseRegistry.register(ValueError)
def handle_value_error(e):
    logging.warning(f"Value anomaly detected: {e}. Coercing to None.")
    return None

def robust_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            resolution = EdgeCaseRegistry.resolve(e)
            if resolution is not None:
                return resolution
            logging.critical(f"Unrecoverable fault: {type(e).__name__}")
            raise AutomationError("System instability reached") from e
    return wrapper