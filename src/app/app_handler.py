import inspect
from typing import Optional

from pojo.auth_pojo import AuthPojo
from pojo.input_pojo import InputPojo
from src.app.base_handler import BaseHandler
from src.models.model_handler import ModelHandler


class AppHandler(BaseHandler):

    def __init__(self, auth: AuthPojo = None, message: InputPojo = None):
        super().__init__()
        self.auth = auth
        self.message = message

        self.client = None

    def main(self):
        try:
            self.client = ModelHandler(self.auth, self.message)
            self.client.initialize_client()

            response = self.client.get_response()

            if response:
                self.done = True

        except Exception as bad_exception:
            class_name = self.__class__.__name__
            method_name = inspect.currentframe().f_code.co_name
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return self.done
