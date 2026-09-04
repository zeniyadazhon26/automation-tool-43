import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name='automation-tool-43', log_file='automation.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Rotating file handler: 5MB per file, keep 3 backups
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=5*1024*1024, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console stream for visibility
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

# Dynamic logging singleton for automation-tool-43
logger = get_logger()