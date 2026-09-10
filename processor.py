from typing import Any, Callable, Dict, Generator, List, Optional

class LoopProcessor:
    def __init__(self, schema_rules: Optional[Dict[str, Callable[[Any], bool]]] = None) -> None:
        self.rules = schema_rules or {
            "id": lambda v: isinstance(v, int) and v > 0,
            "payload": lambda v: isinstance(v, (str, dict)) and bool(v),
            "checksum": lambda v: isinstance(v, str) and len(v) == 8,
        }
        self.quarantine: List[Any] = []

    def validate_item(self, item: Any) -> bool:
        if not isinstance(item, dict):
            return False
        return all(
            key in item and rule(item[key])
            for key, rule in self.rules.items()
        )

    def run_loop(self, input_stream: List[Any]) -> Generator[Dict[str, Any], None, None]:
        for raw_data in input_stream:
            if not self.validate_item(raw_data):
                self.quarantine.append(raw_data)
                continue

            transformed = {
                k: v.strip() if isinstance(v, str) else v
                for k, v in raw_data.items()
            }
            transformed["_status"] = "validated"
            yield transformed
