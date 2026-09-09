import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, default_path: str = "defaults.json"):
        self._defaults = self._load_json(default_path)
        self._config = self._defaults.copy()

    def _load_json(self, path: str) -> Dict[str, Any]:
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {}

    def load(self, override_path: str) -> 'ConfigLoader':
        overrides = self._load_json(override_path)
        self._config.update(overrides)
        return self

    def __getattr__(self, name: str) -> Any:
        return self._config.get(name)

    def __getitem__(self, key: str) -> Any:
        return self._config[key]

    def get(self, key: str, fallback: Any = None) -> Any:
        return self._config.get(key, fallback)

    @property
    def dump(self) -> Dict[str, Any]:
        return dict(self._config)

# Usage:
# cfg = ConfigLoader().load("settings.json")
# print(cfg.api_key)