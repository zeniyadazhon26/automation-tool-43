import logging
import os

class AutoRotatingStream:
    """A file-like stream that handles its own rotation based on size constraints."""
    def __init__(self, filepath: str, max_bytes: int = 2048, backup_count: int = 2):
        self.filepath = filepath
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self._stream = open(self.filepath, "a", encoding="utf-8")
        self._current_size = os.path.getsize(self.filepath) if os.path.exists(self.filepath) else 0

    def write(self, data: str) -> int:
        data_len = len(data.encode("utf-8"))
        if self._current_size + data_len > self.max_bytes:
            self._rotate()
        bytes_written = self._stream.write(data)
        self._stream.flush()
        self._current_size += bytes_written
        return bytes_written

    def flush(self) -> None:
        self._stream.flush()

    def _rotate(self) -> None:
        self._stream.close()
        for i in range(self.backup_count - 1, 0, -1):
            src = f"{self.filepath}.{i}"
            dst = f"{self.filepath}.{i+1}"
            if os.path.exists(src):
                if os.path.exists(dst):
                    os.remove(dst)
                os.rename(src, dst)
        if os.path.exists(self.filepath):
            os.rename(self.filepath, f"{self.filepath}.1")
        self._stream = open(self.filepath, "w", encoding="utf-8")
        self._current_size = 0

def setup_logger(name: str = "automation_tool") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Custom stream-based rotating handler bypassing traditional FileHandlers
    stream = AutoRotatingStream("automation.log", max_bytes=4096, backup_count=3)
    handler = logging.StreamHandler(stream)
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger

if __name__ == "__main__":
    log = setup_logger()
    for j in range(100):
        log.info(f"Automation execution event log sequence counter: {j}")
