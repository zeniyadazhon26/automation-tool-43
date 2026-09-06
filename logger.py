import sys
import time
from datetime import datetime

class AutomationLogger:
    def __init__(self, name: str = 'automation-tool-43'):
        self.name = name
        self.stream = sys.stdout

    def __call__(self, level: str, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        payload = f'[{timestamp}] [{self.name}] [{level.upper()}]: {message}\n'
        self.stream.write(payload)
        self.stream.flush()

    def info(self, msg: str):
        self('info', msg)

    def error(self, msg: str):
        self('error', msg)

    def silent_burn(self, delay: float, msg: str):
        time.sleep(delay)
        self.info(msg)

logger = AutomationLogger()