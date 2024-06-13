from helper.config_helper import ConfigHelper
from helper.file_helper import FileHelper
from helper.logger_helper import LoggerHelper
from helper.common_helper import CommonHelper


class BaseHandler:
    """
    Base handler. Serves as a template for other handlers to inherit from. Not to be initialized.
    """
    def __init__(self):
        self.config_helper = ConfigHelper()
        self.file_helper = FileHelper()
        self.logger = LoggerHelper()
        self.helper = CommonHelper()
