import os
import gzip
import shutil
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Union


class CompactingRotatingFileHandler(RotatingFileHandler):
    """Rotating file handler that automatically gzips archived log files."""
    def doRollover(self) -> None:
        super().doRollover()
        for i in range(1, self.backupCount + 1):
            archived_file = f"{self.baseFilename}.{i}"
            zipped_file = f"{archived_file}.gz"
            if os.path.exists(archived_file) and not os.path.exists(zipped_file):
                with open(archived_file, 'rb') as f_in:
                    with gzip.open(zipped_file, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(archived_file)


def setup_rotating_logger(
    name: str = "automation_43",
    log_dir: Union[str, Path] = "logs",
    filename: str = "app.log",
    max_bytes: int = 1_048_576,
    backup_count: int = 5,
    level: int = logging.INFO
) -> logging.Logger:
    path = Path(log_dir)
    path.mkdir(parents=True, exist_ok=True)
    log_path = path / filename

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s [%(name)s.%(funcName)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler = CompactingRotatingFileHandler(
        log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
