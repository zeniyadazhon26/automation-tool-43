import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str, defaults: Dict[str, Any] = None):
        self.path = path
        self.defaults = defaults or {}
        self._data = {}

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key, self.defaults.get(key))

    def load(self) -> None:
        try:
            if os.path.exists(self.path):
                with open(self.path, 'r') as f:
                    self._data = json.load(f)
            else:
                self._data = {}
        except (json.JSONDecodeError, IOError):
            self._data = {}

    def __repr__(self) -> str:
        return f"ConfigLoader(source={self.path}, keys={list(self._data.keys())})"

def get_config(path: str, defaults: Dict[str, Any]) -> ConfigLoader:
    cfg = ConfigLoader(path, defaults)
    cfg.load()
    return cfg