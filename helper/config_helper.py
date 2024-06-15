import inspect
from configparser import ConfigParser
from typing import Optional

from decorators.decorators import Singleton
from helper.logger_helper import LoggerHelper


@Singleton
class ConfigHelper:
    """
    Provides helper methods for configuration files found either locally or outside.
    """
    def __init__(self, config: ConfigParser = None, option: str = None):
        self.config = config
        self.option = option
        self.logger = LoggerHelper()

        self.commons = "commons"

    def read_ini(self, file_path: str) -> ConfigParser:
        """
        Reads .ini configuration files and returns content read.
        :param file_path: Absolute file location of .ini file
        :return: ConfigParser object
        """
        configuration = ConfigParser()
        configuration.read(file_path)
        self.config = configuration
        return configuration

    def get_value(self, parameter: str = "", option: Optional[str] = None):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = ""

        try:
            if self.config:
                if self.config.has_option(option or self.option, parameter):
                    result = self.config[option or self.option].get(parameter, "")
                else:
                    result = self.config[self.commons].get(parameter, "")
            else:
                self.logger.warning("Missing configuration file from self.config; please ensure config file is read!")

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return result

    def get_boolean(self, parameter: str = "", option: Optional[str] = None):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = False

        try:
            if self.config:
                if self.config.has_option(option or self.option, parameter):
                    result = self.config[option or self.option].getboolean(parameter, False)
                else:
                    result = self.config[self.commons].getboolean(parameter, False)
            else:
                self.logger.warning("Missing configuration file from self.config; please ensure config file is read!")

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return result

    def get_int(self, parameter: str = "", option: Optional[str] = None):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = 0

        try:
            if self.config:
                if self.config.has_option(option or self.option, parameter):
                    result = self.config[option or self.option].getint(parameter, 0)
                else:
                    result = self.config[self.commons].getint(parameter, 0)
            else:
                self.logger.warning("Missing configuration file from self.config; please ensure config file is read!")

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return result
