"""Logging module"""
import logging


class Logger:
    """Logging module"""

    def __init__(self, name: str, filename: str):
        self.name = name
        self.filename = filename
        self.logger = logging.getLogger(name)

        self.setup()

    def info(self, message: str):
        """Log an info message"""
        self.logger.info(message)

    def error(self, message: str):
        """Log an error message"""
        self.logger.error(message)

    def setup(self):
        """Setup the logger with the handlers and the formatter"""
        fs_handler = logging.FileHandler(self.filename)
        std_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            fmt="%(asctime)s [%(name)s] %(levelname)s :: %(message)s"
        )

        handlers = [fs_handler, std_handler]

        for handler in handlers:
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self.logger.setLevel(logging.DEBUG)

        self.logger.propagate = False
