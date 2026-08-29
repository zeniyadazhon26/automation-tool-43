import json
import os
import tempfile
from typing import Any, Dict, Optional

class ConfigLoader:
    def __init__(self, defaults: Optional[Dict[str, Any]] = None) -> None:
        self.defaults = defaults or {}
        self.config: Dict[str, Any] = self.defaults.copy()

    def load(self, filepath: str) -> Dict[str, Any]:
        if not filepath or not os.path.exists(filepath):
            return self.config
        with open(filepath, 'r', encoding='utf-8') as f:
            data: Dict[str, Any] = json.load(f)
        self.config = self._deep_merge(self.config, data)
        return self.config

    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        current: Any = self.config
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        return current

if __name__ == "__main__":
    defaults = {
        "app": {"name": "automation-tool-43", "debug": False},
        "settings": {"timeout": 30}
    }
    loader = ConfigLoader(defaults)
    sample = {"app": {"debug": True}, "settings": {"timeout": 60}}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        json.dump(sample, tmp)
        tmp_path = tmp.name
    try:
        loader.load(tmp_path)
        print(loader.get("app.name"))
        print(loader.get("app.debug"))
        print(loader.get("settings.timeout"))
    finally:
        os.unlink(tmp_path)