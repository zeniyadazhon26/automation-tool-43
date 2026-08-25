import collections
from typing import Any, Dict, List

def process_general_data(data: Any) -> Dict[str, Any]:
    if data is None:
        return {"processed": [], "stats": {"count": 0}, "summary": "No data provided"}
    processed: List[Dict[str, Any]] = []
    stats: Dict[str, Any] = {
        "total_items": 0,
        "types": collections.Counter()
    }
    stack: List[tuple] = [(data, [])]
    while stack:
        current, path = stack.pop()
        if isinstance(current, dict):
            for key, value in current.items():
                stack.append((value, path + [key]))
        elif isinstance(current, (list, tuple)):
            for idx, item in enumerate(current):
                stack.append((item, path + [idx]))
        else:
            path_str = ".".join(str(p) for p in path)
            entry = {
                "path": path_str,
                "value": current,
                "type": type(current).__name__,
                "length": len(current) if isinstance(current, (str, list, dict, tuple)) else None
            }
            processed.append(entry)
            stats["total_items"] += 1
            stats["types"][type(current).__name__] += 1
    processed.sort(key=lambda x: (x["path"].count(".") + 1, x["path"]))
    type_counts = dict(stats["types"])
    return {
        "processed": processed,
        "stats": {
            "total_items": stats["total_items"],
            "type_counts": type_counts
        },
        "summary": f"Processed {stats['total_items']} items across {len(type_counts)} types"
    }

def get_values_by_type(processed_result: Dict[str, Any], target_type: str) -> List[Any]:
    return [
        item["value"] for item in processed_result.get("processed", [])
        if item.get("type") == target_type
    ]

def summarize_data(processed_result: Dict[str, Any]) -> str:
    stats = processed_result.get("stats", {})
    return f"Total: {stats.get('total_items', 0)}, Types: {stats.get('type_counts', {})}"
