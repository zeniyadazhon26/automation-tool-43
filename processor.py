from typing import List, Dict, Union, Optional, Callable

class DataProcessor:
    """Process raw streams using polymorphic functional mapping."""

    def __init__(self, transformers: Optional[List[Callable[[str], str]]] = None) -> None:
        self._pipeline: List[Callable[[str], str]] = transformers or []

    def add_step(self, func: Callable[[str], str]) -> None:
        """Append a processing function to the internal chain."""
        self._pipeline.append(func)

    def execute(self, data: List[str]) -> List[str]:
        """Transform data batches through the pipeline chain."""
        return [self._apply_chain(item) for item in data]

    def _apply_chain(self, value: str) -> str:
        """Recursive reduction of value through pipeline steps."""
        for step in self._pipeline:
            value = step(value)
        return value

def slugify(text: str) -> str:
    """Convert strings to lowercase kebab-case format."""
    return "-".join(text.lower().split())

def scrub_nulls(text: str) -> str:
    """Remove all null-byte characters from strings."""
    return text.replace("\x00", "")

if __name__ == "__main__":
    proc = DataProcessor(transformers=[scrub_nulls, slugify])
    results: List[str] = proc.execute(["Hello World", "Automation Tool 43"])
    print(results)