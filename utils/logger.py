import os
import logging
 
class CustomFileHandler(logging.FileHandler):
    def __init__(self, filename, mode='a', maxBytes=500 * 1024 * 1024, encoding=None, delay=False):
        self.maxBytes = maxBytes
        super().__init__(filename, mode, encoding, delay)
   
    def emit(self, record):
        try:
            if os.path.exists(self.baseFilename) and os.path.getsize(self.baseFilename) >= self.maxBytes:
                self.stream.close()
                os.remove(self.baseFilename)
                self.stream = self._open()
        except Exception:
            self.handleError(record)
        super().emit(record)
 
class LoggerHandler:
    name: str = __name__
    logger = logging.getLogger(name)
 
    def __post_init__(self):
        self.logger.setLevel(logging.INFO)
 
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
 
        file_handler = CustomFileHandler("log.log", mode="a", maxBytes=500 * 1024 * 1024)
        file_handler.setLevel(logging.INFO)
 
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
 
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
 
    def get_logger(self):
        return self.logger