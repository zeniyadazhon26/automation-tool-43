import fnmatch
from typing import Any, Dict, Tuple, Union

class PathMap:
    """A path-addressable nested data wrapper with glob-based querying."""

    def __init__(self, data: Union[Dict, list, Any]):
        self.flat_data: Dict[Tuple[Union[str, int], ...], Any] = {}
        self._decompose(data, ())

    def _decompose(self, item: Any, path: Tuple[Union[str, int], ...]) -> None:
        if isinstance(item, dict):
            for k, v in item.items():
                self._decompose(v, path + (k,))
        elif isinstance(item, (list, tuple)):
            for i, v in enumerate(item):
                self._decompose(v, path + (i,))
        else:
            self.flat_data[path] = item

    def query(self, pattern: str) -> Dict[str, Any]:
        """Query flattened paths using a slash-separated glob pattern (e.g. 'users/*/profile/name')."""
        results = {}
        for path, value in self.flat_data.items():
            path_str = "/".join(map(str, path))
            if fnmatch.fnmatchcase(path_str, pattern):
                results[path_str] = value
        return results

    def reconstruct(self) -> Dict[str, Any]:
        """Reconstruct a nested dictionary structure from the flat representation."""
        root: Dict[str, Any] = {}
        for path, value in self.flat_data.items():
            current = root
            for part in path[:-1]:
                current = current.setdefault(str(part), {})
            if path:
                current[str(path[-1])] = value
        return root