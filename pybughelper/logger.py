import time
import os
from datetime import datetime

pyos = os

class BugLogger:
    def __init__(self, log_file="system.log"):
        self.log_file = log_file

    def _write_log(self, level, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        with open(self.log_file, "a") as f:
            f.write(log_entry)

    def info(self, message):
        self._write_log("INFO", message)

    def error(self, message):
        self._write_log("ERROR", message)

    @staticmethod
    def time_this(func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            print(f"Function '{func.__name__}' took {end - start:.6f} seconds")
            return result
        return wrapper
