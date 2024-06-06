import inspect

import pymongo

from constants.constants import SUBTASK_CONST, SUBTASK_DB_CONST
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

                self.client = pymongo.MongoClient(authy.get("db_form", ""))
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
                self.db = self.client.cosmic_works
                self.collection = self.db.products

                self.logger.info(f"Class {class_name} of method {method_name} successfully executed.")
                success = True

            else:
                self.logger.warning(f"Class {class_name} of method {method_name}: no self.client initialized.")

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return success

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

            elif subtask == SUBTASK_DB_CONST.CREATE:
                self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                 f"Initializing methods.")
                result = self.db_helper.create_one_document(self.message.document)
                self.message.subtask_completed = True
                return result

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")
