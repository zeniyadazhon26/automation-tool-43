import json
from typing import Any, Dict, List, Union
from functools import reduce

def deep_extract(data: Dict[str, Any], path: str, delimiter: str = '.') -> Any:
    """extract nested values using dot-notation paths"""
    try:
        return reduce(lambda d, key: d.get(key, {}) if isinstance(d, dict) else None, path.split(delimiter), data)
    except Exception:
        return None

def sanitize_payload(obj: Any) -> Any:
    """recursively clean input to ensure json-serializable types"""
    if isinstance(obj, dict):
        return {str(k): sanitize_payload(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [sanitize_payload(i) for i in obj]
    if isinstance(obj, (int, float, str, bool)) or obj is None:
        return obj
    return str(obj)

class DataPipeline:
    """creative pipe-based data transformation tool"""
    def __init__(self, initial_data: Any):
        self.stream = initial_data

    def pipe(self, func: callable, *args, **kwargs) -> 'DataPipeline':
        self.stream = func(self.stream, *args, **kwargs)
        return self

    def collect(self) -> Any:
        return self.stream

def format_json_pretty(data: Any) -> str:
    """standardized serialization wrapper"""
    return json.dumps(sanitize_payload(data), indent=4, sort_keys=True)