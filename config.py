import os
from typing import Dict, Any, Union

class ConfigLoader:
    """Factory for retrieving operational parameters from environment."""

    def __init__(self, prefix: str = "AUTO_43_") -> None:
        self.prefix: str = prefix
        self._cache: Dict[str, str] = {}

    def get_setting(self, key: str, default: Union[str, int, None] = None) -> Any:
        """Dynamic resolution of configuration values with fallback."""
        env_key: str = f"{self.prefix}{key.upper()}"
        value: Union[str, None] = os.environ.get(env_key, str(default) if default else None)
        
        if value and value.isdigit():
            return int(value)
        return value

def load_defaults() -> Dict[str, Any]:
    """Collection of baseline runtime constants for automation."""
    loader: ConfigLoader = ConfigLoader()
    return {
        "timeout": loader.get_setting("timeout", 30),
        "retries": loader.get_setting("retries", 3),
        "mode": loader.get_setting("mode", "development")
    }

SETTINGS: Dict[str, Any] = load_defaults()