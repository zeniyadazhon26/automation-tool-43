import os
from typing import Any, Dict

class ConfigLoader:
    """A magical recursive dictionary configurator."""
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def load_env(self, prefix: str = 'APP_'):
        """Overlay environment variables onto existing config."""
        for key in self._data:
            env_key = f"{prefix}{key.upper()}"
            if env_key in os.environ:
                self._data[key] = os.environ[env_key]
        return self

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"config entry '{name}' is missing")

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    @property
    def registry(self) -> Dict[str, Any]:
        return self._data

def get_config():
    defaults = {
        "host": "localhost",
        "port": 8080,
        "debug": False,
        "db_url": "sqlite:///:memory:"
    }
    return ConfigLoader(defaults).load_env()