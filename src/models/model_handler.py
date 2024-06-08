import inspect
from typing import Optional

from openai.lib.azure import AzureOpenAI

from constants.constants import SUBTASK_CONST
from pojo.auth_pojo import AuthPojo
from pojo.input_pojo import InputPojo
from src.app.base_handler import BaseHandler


class ModelHandler(BaseHandler):

    def __init__(self, auth: AuthPojo = None, message: InputPojo = None):
        super().__init__()
        self.auth = auth
        self.message = message
        self.client = None

    def initialize_client(self):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        client = None

        try:
            if self.auth:
                authy = self.auth.to_json()

                client = AzureOpenAI(
                    azure_endpoint=authy.get("endpoint", None),
                    api_key=authy.get("openai_key", None),
                    api_version=authy.get("api_version", None)
                )

                self.message.client_exists = True
                self.message.task_completed = True
                self.client = client

            else:
                self.logger.warning("No authentication keys or information received. Cannot initialize client.")

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return client

    def get_response(self):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        response = None

        try:
            if self.message and self.client:
                message = self.message.to_json()
                role = message.get("role", {}).to_json()

                response = self.client.chat.completions.create(
                    model=role.get("model", "gpt-4").value,
                    messages=message.get("messages", [{}])
                )

                self.message.last_message = response.choices[0].message.content

            else:
                self.logger.warning("No message pojo or / and client initialized. Cannot obtain response.")

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return response

    def main(self):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name

        try:
            subtask = self.message.role.subtask

            if subtask == SUBTASK_CONST.CLIENT:
                if self.client:
                    self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                     f"Declaring sub-task completed.")
                    self.message.subtask_completed = True
                    return None

                else:
                    raise Exception(f"No client found for {self.client}")

            elif subtask == SUBTASK_CONST.RESPONSE:
                self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                 f"Initializing methods.")
                result = self.get_response()
                self.message.subtask_completed = True
                return result

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

