import sys
import time
import inspect
from typing import Any, Dict, List, Optional, Generator
from contextlib import contextmanager


class SpectrumLogger:
    """A colorful, scope-aware logger designed for dynamic runtime inspection."""

    _PALETTE: List[str] = ["\033[36m", "\033[33m", "\033[35m", "\033[32m", "\033[34m"]
    _RESET: str = "\033[0m"

    def __init__(self, name: str = "auto-43") -> None:
        self.name: str = name
        self.history: List[Dict[str, Any]] = []
        self._depth: int = 0

    def _hash_color(self, token: str) -> str:
        """Derives an ANSI color code deterministically from an input string token."""
        index: int = sum(ord(c) for c in token) % len(self._PALETTE)
        return self._PALETTE[index]

    def log(self, message: str, level: str = "INFO", **extra: Any) -> Dict[str, Any]:
        """Emits a structured log record decorated with caller scope and color palette.

        Args:
            message: Text description of the log event.
            level: Severity indicator string.
            **extra: Additional metadata attributes attached to the payload.

        Returns:
            Dict containing formatted timestamp, source frame, and record metadata.
        """
        caller_frame = inspect.currentframe()
        source_func: str = "unknown"
        if caller_frame and caller_frame.f_back:
            source_func = caller_frame.f_back.f_code.co_name

        color: str = self._hash_color(source_func)
        indent: str = "  " * self._depth
        timestamp: float = time.time()

        record: Dict[str, Any] = {
            "timestamp": timestamp,
            "level": level.upper(),
            "scope": source_func,
            "message": message,
            "extra": extra
        }
        self.history.append(record)

        formatted_output: str = (
            f"{color}[{self.name}][{record['level']}][{source_func}]{self._RESET} "
            f"{indent}{message}"
        )
        print(formatted_output, file=sys.stderr)
        return record

    @contextmanager
    def scope(self, section_name: str) -> Generator[None, None, None]:
        """Context manager to auto-indent and bracket a logical execution scope.

        Args:
            section_name: Name of the nested execution block.
        """
        self.log(f">>> Entering {section_name}", level="DEBUG")
        self._depth += 1
        try:
            yield
        finally:
            self._depth = max(0, self._depth - 1)
            self.log(f"<<< Exiting {section_name}", level="DEBUG")


def get_logger(name: str = "default") -> SpectrumLogger:
    """Factory helper to instantiate a SpectrumLogger instance."""
    return SpectrumLogger(name=name)
