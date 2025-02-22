import logging
from dataclasses import dataclass

@dataclass
class LoggerHandler:
    name: str = __name__

    def __post_init__(self):
        
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)

    def get_logger(self):
        """Devuelve el logger configurado"""
        return self.logger
