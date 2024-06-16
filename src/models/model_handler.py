import inspect
import json
import time
from typing import Optional

from openai.lib.azure import AzureOpenAI
from pymongo.command_cursor import CommandCursor

from constants.constants import SUBTASK_CONST, SUBTASK_EMBED_CONST, FLAG_CONST, TASK_CONST
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
        # print("get_res_1")

        try:
            if self.message and self.client:
                message = self.message.to_json()
                role = message.get("role", {}).to_json()
                messages=message.get("messages", [{}])
                # print("msg_role_1:",messages)
                # # print("msg_role_2:",role)
                # print("self.client",self.client)

                response = self.client.chat.completions.create(
                    # model=role.get("model", "gpt-4").value,
                    model=role.get("model", "completions").value,
                    # model = "completions",
                    messages=message.get("messages", [{}])
                )
                # print('res_2')
                # print('response',response)

                self.message.last_message = response.choices[0].message.content

            else:
                self.logger.warning("No message pojo or / and client initialized. Cannot obtain response.")

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return response

    # def generate_embeddings(self, message: str = None):
    def generate_embeddings(self, message: str = None):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = None
        #Added by wyapb
        # print(self.message.role.embeddings.value)
        #End add

        try:
            input_msg = message or self.message.embed_message
            response = self.client.embeddings.create(input=input_msg,
                                                     model=self.message.role.embeddings.value)
            result = response.data[0].embedding
            time.sleep(0.5)

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return result

    def rag_vector_search(self, query: CommandCursor = None):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = None

        try:
            if query:
                information = ""

                for info in query:
                    if "contentVector" in info.get("document"):
                        del info.get("document")["contentVector"]
                        information += json.dumps(info.get("document"), indent=4, default=str) + "\n\n"

                prompt = self.message.prompt + information

                messages = [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": self.message.query}
                ]

                result = self.client.chat.completions.create(messages=messages,
                                                             model=self.message.role.model.value)

                self.message.last_message = result.choices[0].message.content

            else:
                self.logger.warning(f"Class {class_name} of method {method_name}: Query embeddings is empty.")

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: "
                              f"{bad_exception}")

        finally:
            return result

    def main(self, attachments=None):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = None

        try:
            subtask = self.message.role.subtask

            if subtask == SUBTASK_CONST.CLIENT:
                if self.client:
                    self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                     f"Declaring sub-task completed.")
                    self.message.subtask_completed = True

                else:
                    raise Exception(f"No client found for {self.client}")

            elif subtask == SUBTASK_CONST.RESPONSE:
                self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                 f"Initializing methods.")
                result = self.get_response()
                self.message.subtask_completed = True

            elif subtask == SUBTASK_EMBED_CONST.GENERATE:
                self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                 f"Initializing methods.")
                result = self.generate_embeddings()
                self.message.subtask_completed = True

            elif subtask == SUBTASK_CONST.RESPONSE_CONTEXT:
                self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                 f"Initializing methods.")

                if self.message.db_exists:
                    self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                     f"CosmosDB initialized. Initializing methods.")

                    vectors = attachments.main(attachments=self)
                    result = self.rag_vector_search(query=vectors)

                    self.message.subtask_completed = True

                else:
                    self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                     f"CosmosDB not initialized. Initializing.")

                    self.message.role.flag = FLAG_CONST.INIT_DATABASE
                    self.helper.adjust_tasking(message=self.message,
                                               task=TASK_CONST.DATABASE,
                                               subtask=SUBTASK_EMBED_CONST.SEARCH,
                                               revert=False)

            else:
                self.logger.warning(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                    f"Unable to determine correct sub-tasking. Failing.")
                self.message.subtask_completed = True

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return result
