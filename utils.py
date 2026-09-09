import re
from datetime import datetime
from typing import Any

class FluidMap(dict):
    """A dictionary wrapper offering attribute access and dynamic string type coercion."""

    _TRUE_PATTERNS = re.compile(r"^(true|yes|on|1)$", re.IGNORECASE)
    _FALSE_PATTERNS = re.compile(r"^(false|no|off|0)$", re.IGNORECASE)
    _ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(\.\d+)?)?Z?$")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in list(self.items()):
            self[k] = self._coerce(v)

    def _coerce(self, val: Any) -> Any:
        if isinstance(val, dict):
            return FluidMap(val)
        if isinstance(val, list):
            return [self._coerce(item) for item in val]
        if isinstance(val, str):
            val_strip = val.strip()
            if self._TRUE_PATTERNS.match(val_strip):
                return True
            if self._FALSE_PATTERNS.match(val_strip):
                return False
            if val_strip.isdigit():
                return int(val_strip)
            try:
                return float(val_strip)
            except ValueError:
                pass
            if self._ISO_DATE.match(val_strip):
                try:
                    return datetime.fromisoformat(val_strip.replace("Z", "+00:00"))
                except ValueError:
                    pass
        return val

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'FluidMap' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = self._coerce(value)

    def __delattr__(self, name: str) -> None:
        try:
            del self[name]
        except KeyError:
            raise AttributeError(f"'FluidMap' object has no attribute '{name}'")
