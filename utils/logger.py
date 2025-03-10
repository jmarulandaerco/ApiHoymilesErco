import logging
from dataclasses import dataclass
import os

from utils.configHandler import ConfigHandler
from utils.helper import HelperReport


# LOG_FILE = "log.log"
# MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB

# def check_log_size():
#     if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > MAX_LOG_SIZE:
#         os.remove(LOG_FILE)  # Elimina el archivo si supera el tamaño máximo

@dataclass
class LoggerHandler:
    """
    Handles application logging by configuring console and file loggers.

    Attributes:
        name (str): Logger name, defaults to `__name__`.
        logger (logging.Logger): Configured logger instance.

    Methods:
        get_logger() -> logging.Logger: Returns the configured logger instance.
    """
    name: str = __name__

    def __post_init__(self):
        helper = HelperReport()
        helper.check_log_sizes()
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        configHandler=ConfigHandler("config.ini") 
        file_handler = logging.FileHandler(str(configHandler.get_name_log()), mode="a")
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger