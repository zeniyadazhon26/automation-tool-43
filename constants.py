from typing import Final, Dict, List, Any

# Configuration constants for the automation-tool-43 engine
# We utilize Final types to ensure runtime integrity of constants

MAX_RETRIES: Final[int] = 5
TIMEOUT_SECONDS: Final[float] = 30.5

DEFAULT_HEADERS: Final[Dict[str, str]] = {
    "User-Agent": "automation-tool-43/1.0.0",
    "Content-Type": "application/json"
}

ALLOWED_PROTOCOLS: Final[List[str]] = ["http", "https", "ftp"]

# Dynamic registry mapping for internal processors
PROCESSOR_MAP: Final[Dict[str, Any]] = {
    "data_sink": "core.DataProcessor",
    "event_bus": "handler.EventHandler",
    "validator": "validators.SchemaValidator"
}

def get_timeout_multiplier(factor: float) -> float:
    """
    Calculate a modified timeout based on a dynamic input factor.

    Args:
        factor: A float multiplier to scale the base timeout constant.

    Returns:
        A scaled float value representing the adjusted timeout.
    """
    return float(TIMEOUT_SECONDS * factor)