import logging
from datetime import datetime
from config import LOG_LEVEL, LOG_FORMAT, LOG_DATE_FORMAT, RESULTS_DIR
import os

class Logger:

    def __init__(self, name: str = 'payload_tester', log_to_file: bool = True):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, LOG_LEVEL))

        #Handler

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        #file handler

        if log_to_file:
            log_file = os.path.join(RESULTS_DIR, f'scan_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        self.logger.critical(message)
        