import os
import json
from typing import Any, Dict

class ConfigError(Exception):
    """Custom exception for edge cases in config management."""
    pass

def load_config(filepath: str) -> Dict[str, Any]:
    """
    Loads configuration with paranoid integrity checks.
    Unusual approach: self-healing defaults on corruption.
    """
    if not os.path.exists(filepath):
        return {"status": "initialized", "retry_limit": 3}

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        # Edge case: empty file or invalid types
        if not isinstance(data, dict):
            raise ValueError("Config file must contain a mapping")
            
        return data
    except (json.JSONDecodeError, ValueError, PermissionError) as e:
        # Creative handling: treat catastrophic corruption as a signal to reset
        # Logged to console as a temporary side-effect of non-standard error strategy
        print(f"Config anomaly detected: {e}. Resetting to baseline.")
        return {
            "status": "recovered",
            "error_trace": str(e)[:50],
            "timestamp": "now"
        }

def sanitize_key(key: Any) -> str:
    """
    Converts non-string keys into strings, a defensive programming measure.
    """
    try:
        return str(key).strip().lower()
    except Exception:
        return "unknown_key_type"