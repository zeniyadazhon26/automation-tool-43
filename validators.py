from typing import Any, Callable, Dict, Optional

class DataValidator:
    def __init__(self):
        self._registry: Dict[str, Callable[[Any], bool]] = {}

    def register(self, name: str, predicate: Callable[[Any], bool]) -> None:
        self._registry[name] = predicate

    def validate(self, name: str, value: Any) -> bool:
        if name not in self._registry:
            return False
        try:
            return self._registry[name](value)
        except Exception:
            return False

    def pipeline(self, data: Dict[str, Any], schema: Dict[str, str]) -> Dict[str, bool]:
        return {k: self.validate(schema[k], data.get(k)) for k in schema}

    @staticmethod
    def chain(*validators: Callable[[Any], bool]) -> Callable[[Any], bool]:
        return lambda x: all(v(x) for v in validators)

def create_validator() -> DataValidator:
    instance = DataValidator()
    instance.register("non_empty", lambda x: bool(x) and len(str(x)) > 0)
    instance.register("numeric", lambda x: isinstance(x, (int, float)))
    instance.register("email", lambda x: isinstance(x, str) and "@" in x and "." in x)
    return instance

def sanitize(data: Dict[str, Any], keys: list) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if k in keys and v is not None}