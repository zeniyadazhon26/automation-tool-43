import functools
import time
import logging

logger = logging.getLogger('automation-tool-43')

class OptimizationError(Exception):
    """Custom base exception for performance boundary breaches."""
    pass

def time_limit_exceeded(func):
    """
    Decorator to enforce execution time boundaries.
    Uses a non-blocking performance threshold.
    """
    limit = 0.5
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        
        if elapsed > limit:
            logger.warning(f"Function {func.__name__} exceeded {limit}s")
            raise OptimizationError(f"Latency threshold of {limit}s breached: {elapsed:.4f}s")
            
        return result
    return wrapper

class CacheOverflowException(OptimizationError):
    """Raised when in-memory registry exceeds allocated bounds."""
    pass

def circuit_breaker(state):
    """
    High-performance state check for avoiding redundant processing.
    """
    if state.get('busy', False):
        raise OptimizationError("System is under heavy load; processing deferred")

# Dynamic registry of performance-critical failures
_registry = {
    'max_depth': 1024,
    'timeout_default': 0.5
}

def get_performance_registry():
    return _registry.copy()