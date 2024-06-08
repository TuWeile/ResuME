import inspect
import os.path
from pathlib import Path

from decorators.decorators import Singleton
from helper.logger_helper import LoggerHelper


@Singleton
class FileHelper:
    """
    Provides helper methods for file moving, deletion, creation, amendment methods
    """
    def __init__(self):
        self.logger = LoggerHelper()

    def resolve_path(self, file_name: str, depth: int) -> str:
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = None

        try:
            abs_filepath = os.path.join(Path(__file__).resolve().parents[depth], "config")
            result = os.path.join(abs_filepath, file_name)

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return result

