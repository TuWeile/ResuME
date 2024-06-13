import inspect

from constants.constants import TASK_CONST
from decorators.decorators import Singleton
from pojo.auth_pojo import AuthPojo
from pojo.input_pojo import InputPojo
from pojo.purpose_pojo import PurposePojo
from src.app.base_handler import BaseHandler
from src.db.db_handler import DBHandler
from src.models.langchain_handler import LangchainHandler
from src.models.model_handler import ModelHandler
 

@Singleton
class TaskFactory(BaseHandler):
    def __init__(self, auth: AuthPojo = None, message: InputPojo = None):
        super().__init__()
        self.auth = auth
        self.message = message

    def main(self):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name

        try:
            message = self.message.to_json()

            if type(message.get("role").to_json()) == dict:
                role = message.get("role").to_json()
                task = role.get("task", None)

                # NOTE: Could be better coded than if-else clauses, but this will do for now.

                if task == TASK_CONST.CONNECT:
                    self.logger.info(f"Class {class_name} of method {method_name}: {task} determined. "
                                     f"Declaring ModelHandler class.")
                    return ModelHandler(self.auth, self.message)

                elif task == TASK_CONST.DATABASE:
                    self.logger.info(f"Class {class_name} of method {method_name}: {task} determined. "
                                     f"Declaring DBHandler class.")
                    return DBHandler(self.auth, self.message)

                elif task == TASK_CONST.LANGCHAIN:
                    self.logger.info(f"Class {class_name} of method {method_name}: {task} determined. "
                                     f"Declaring DBHandler class.")
                    return LangchainHandler(self.auth, self.message)

                else:
                    raise Exception(f"Unable to find valid task class with {task}")

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")
