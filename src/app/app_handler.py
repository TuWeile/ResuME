import inspect
from typing import Optional

from pojo.auth_pojo import AuthPojo
from pojo.input_pojo import InputPojo
from src.app.base_handler import BaseHandler
from src.app.factory.task_factory import TaskFactory
from src.models.model_handler import ModelHandler
from src.db.db_handler import DBHandler


class AppHandler(BaseHandler):

    def __init__(self, auth: AuthPojo = None, message: InputPojo = None):
        super().__init__()
        self.auth = auth
        self.message = message

        self.factory = None
        self.task = None

    def main(self):
        try:
            self.factory = TaskFactory(self.auth, self.message)
            self.task = self.factory.main()

            if self.task:
                self.task.initialize_client()

            subtask_clause = self.message.role.subtask and not self.message.subtask_completed

            while self.message.task_completed and subtask_clause:
                result = self.task.main()
                subtask_clause = self.message.role.subtask and not self.message.subtask_completed

            if self.message.task_completed and self.message.subtask_completed:
                self.message.done = True

        except Exception as bad_exception:
            class_name = self.__class__.__name__
            method_name = inspect.currentframe().f_code.co_name
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return result
