import inspect
from typing import Optional

import certifi
import pymongo

from constants.constants import SUBTASK_CONST, SUBTASK_DB_CONST, SUBTASK_EMBED_CONST, FLAG_CONST, TASK_CONST
from helper.db_helper import DBHelper
from pojo.auth_pojo import AuthPojo
from pojo.input_pojo import InputPojo
from src.app.base_handler import BaseHandler


class DBHandler(BaseHandler):

    def __init__(self, auth: AuthPojo = None, message: InputPojo = None):
        super().__init__()
        self.auth = auth
        self.message = message

        self.db_helper = None

        self.client = None
        self.db = None
        self.collection = None

    def initialize_client(self):
        """
        TBA explanation on what this code does
        """
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        client = None

        try:
            if self.auth:
                authy = self.auth.to_json()

                self.client = pymongo.MongoClient(authy.get("db_form", ""), tlsCAFile=certifi.where())
                status = self.client_pre_scrap_actions()

                if status:
                    self.message.db_exists = True
                    self.message.task_completed = True
                    self.db_helper = DBHelper(self.client, self.db, self.collection)

                else:
                    self.logger.warning(f"Class {class_name} of method {method_name}: Unable to initialize pre-scrap. "
                                        f"Voiding client session with MongoDB.")
                    self.client = None

            else:
                self.logger.warning(f"Class {class_name} of method {method_name}: No authentication info given.")

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return client

    def client_pre_scrap_actions(self) -> bool:
        """
        TBA explanation on what this code does
        """
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        success = False

        try:
            if self.client:
                db_name = self.message.database_name
                collection_name = self.message.collection_name

                self.db = self.client[db_name]
                self.collection = self.db[collection_name]

                self.logger.info(f"Class {class_name} of method {method_name} successfully executed.")
                success = True

            else:
                self.logger.warning(f"Class {class_name} of method {method_name}: no self.client initialized.")

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return success

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

            elif subtask == SUBTASK_DB_CONST.CREATE:
                self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                 f"Initializing methods.")
                result = self.db_helper.create_one_document(self.message.documents)
                self.message.subtask_completed = True
            
            elif subtask == SUBTASK_DB_CONST.READ:
                self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                 f"Initializing methods.")
                result = self.db_helper.read_one_document(self.message.read_ids)
                self.message.subtask_completed = True

            elif subtask == SUBTASK_DB_CONST.UPDATE:
                self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                 f"Initializing methods.")
                result = self.db_helper.update_one_document(self.message.read_ids)
                self.message.subtask_completed = True
            
            elif subtask == SUBTASK_DB_CONST.DELETE:
                self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                 f"Initializing methods.")
                result = self.db_helper.delete_one_document(self.message.read_ids)
                self.message.subtask_completed = True
            
            elif subtask == SUBTASK_DB_CONST.FILTER:
                self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                 f"Initializing methods.")
                result = self.db_helper.find_documents(self.message.read_ids)
                self.message.subtask_completed = True

            elif subtask == SUBTASK_EMBED_CONST.VECTORIZE_UPDATE:
                self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                 f"Initializing methods.")

                if self.message.client_exists:
                    self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                     f"OpenAI Client initialized. Initializing methods.")

                    result = self.db_helper.vectorize_and_update_documents(client=attachments)
                    self.message.subtask_completed = True

                else:
                    self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                     f"OpenAI Client not initialized. Initializing.")

                    self.message.role.flag = FLAG_CONST.INIT_CLIENT
                    self.helper.adjust_tasking(message=self.message,
                                               task=TASK_CONST.CONNECT,
                                               subtask=SUBTASK_CONST.CLIENT,
                                               revert=False)

            elif subtask == SUBTASK_EMBED_CONST.CREATE_INDEX:
                self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                 f"Initializing methods.")
                result = self.db_helper.create_vector_index(self.message.vector_index)
                self.message.subtask_completed = True

            elif subtask in [SUBTASK_EMBED_CONST.SEARCH, SUBTASK_CONST.RESPONSE_CONTEXT]:
                self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                 f"Initializing methods.")

                if self.message.client_exists:
                    self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                     f"OpenAI Client initialized. Initializing methods.")

                    result = self.db_helper.vector_search(client=attachments,
                                                          query=self.message.query,
                                                          num_results=self.message.k_search_value)
                    self.message.subtask_completed = True

                else:
                    self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                     f"OpenAI Client not initialized. Initializing.")

                    self.message.role.flag = FLAG_CONST.INIT_CLIENT
                    self.helper.adjust_tasking(message=self.message,
                                               task=TASK_CONST.CONNECT,
                                               subtask=SUBTASK_CONST.CLIENT,
                                               revert=False)

            else:
                self.logger.warning(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                    f"Unable to determine correct sub-tasking. Failing.")
                self.message.subtask_completed = True

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return result
        #     self.client.drop_database("cosmic_works")
        #     self.client.close()
