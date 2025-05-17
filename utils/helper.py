from dataclasses import dataclass, field
import os
from datetime import datetime
from utils.configHandler import ConfigHandler


@dataclass
class HelperReport:
    """
    Manages log file size and ensures it does not exceed a defined limit.

    Attributes:
        LOG_FILE (str): Path to the log file.
        MAX_LOG_SIZE (int): Maximum allowed log file size in bytes.

    Methods:
        check_log_sizes(): Deletes the log file if it exceeds the maximum size.
    """
    LOG_FILE: str = field(init=False)
    MAX_LOG_SIZE: int = field(init=False)

    def __post_init__(self):
        config_handler = ConfigHandler("config.ini")
        self.LOG_FILE = str(config_handler.get_name_log())
        self.MAX_LOG_SIZE = int(config_handler.get_log_size())

    def check_log_sizes(self):
        if os.path.exists(self.LOG_FILE) and os.path.getsize(self.LOG_FILE) > self.MAX_LOG_SIZE:
            os.remove(self.LOG_FILE)

    def round_time_down(self,dt:datetime, interval_minutes:int):
        minutes = dt.minute
        rounded_minutes = (minutes // interval_minutes) * interval_minutes
        return dt.replace(minute=rounded_minutes, second=0, microsecond=0)