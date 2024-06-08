import inspect
import random
import string
import time

from constants.constants import TASK_CONST
from decorators.decorators import Singleton
from helper.file_helper import FileHelper
from helper.logger_helper import LoggerHelper
from pojo.input_pojo import InputPojo


@Singleton
class CommonHelper:
    """
    Provides helper methods for common and generic methods that can be applied in classes
    """

    def __init__(self) -> None:
        self.logger = LoggerHelper()
        self.file_helper = FileHelper()
    
    def get_id_random(self, length: int = 16):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = None

        try:
            characters = string.ascii_letters + string.digits
            result = ''.join(random.choice(characters) for _ in range(length))
        
        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")
        
        finally:
            return result

    def get_current_time(self):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = None

        try:
            result = int(time.time())

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")
        
        finally:
            return result

    def dict_remove_null_values(self, input_dict: dict = None):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = None

        try:
            result = {k: v for k, v in input_dict.items() if v is not None}
        
        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")
        
        finally:
            return result

    def adjust_tasking(self, message: InputPojo = None, task: TASK_CONST = None, subtask = None, revert: bool = False):
        # TODO: Requires refactoring as per PurposePojo TODO.
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name

        try:
            if message:
                if revert and (message.role.prev_task and message.role.prev_subtask):
                    message.role.task = message.role.prev_task
                    message.role.subtask = message.role.prev_subtask

                    message.role.prev_task = None
                    message.role.prev_subtask = None

                elif not revert:
                    message.role.prev_task = message.role.task
                    message.role.prev_subtask = message.role.subtask

                    message.role.task = task
                    message.role.subtask = subtask

                else:
                    raise Exception("Revert argument given as true despite lack of previous tasking.")

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")
            raise Exception("Error in adjusting tasking.")
