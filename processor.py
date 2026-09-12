import logging
import os
import sys
from logging.handlers import RotatingFileHandler


class ResourceAwareFormatter(logging.Formatter):
    def format(self, record):
        # Dynamically inject current process ID into each log record
        record.proc_info = f"[PID:{os.getpid()}]"
        return super().format(record)


def setup_rotating_logger(
    logger_name: str = "automation_tool",
    log_file: str = "app.log",
    max_bytes: int = 1048576,
    backup_count: int = 3,
) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    log_format = "%(asctime)s %(proc_info)s [%(levelname)s] %(message)s"
    formatter = ResourceAwareFormatter(log_format)

    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


if __name__ == "__main__":
    log = setup_rotating_logger()
    log.info("Logger initialized with rotating handler.")
    log.debug("Debug entry targeting the log file.")