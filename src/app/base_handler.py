from helper.config_helper import ConfigHelper
from helper.file_helper import FileHelper
from helper.logger_helper import LoggerHelper


class BaseHandler:
    """
    Base handler. Serves as a template for other handlers to inherit from. Not to be initialized.
    """
    def __init__(self):
        self.done = False

        self.config_helper = ConfigHelper()
        self.file_helper = FileHelper()
        self.logger = LoggerHelper()
