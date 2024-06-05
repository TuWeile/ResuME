import logging
from datetime import datetime

from decorators.decorators import Singleton


@Singleton
class LoggerHelper:
    def __init__(self, logfile_path: str = f"../var/log/{datetime.now().strftime('%Y%m%d')}.txt") -> None:
        """
        Initializes the logger class interface which will send application logs to a particular location in os.
        :param logfile_path: The string value of that particular location in os.
        """
        self.log_file = logfile_path
        self.logger = logging.getLogger(f"{self.__class__.__name__}_{id(self)}")
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

            file_handler = logging.FileHandler(logfile_path)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)

    def __del__(self) -> None:
        """
        Always ensures that the handlers are closed when the instance is destroyed.
        :return: null
        """

        handlers = self.logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.logger.removeHandler(handler)

    def debug(self, message: str):
        """
        Construction of debug message for logging for write.
        :param message: String value of message to be written.
        :return: null
        """
        self.logger.debug(message)

    def info(self, message: str):
        """
        Construction of info message for logging for write.
        :param message: String value of message to be written.
        :return: null
        """
        self.logger.info(message)

    def warning(self, message: str):
        """
        Construction of warning message for logging for write.
        :param message: String value of message to be written.
        :return: null
        """
        self.logger.warning(message)

    def error(self, message: str):
        """
        Construction of error message for logging for write.
        :param message: String value of message to be written.
        :return: null
        """
        self.logger.error(message)
