import inspect

import pymongo

from pojo.auth_pojo import AuthPojo
from pojo.input_pojo import InputPojo
from src.app.base_handler import BaseHandler


class DBHandler(BaseHandler):

    def __init__(self, auth: AuthPojo = None, message: InputPojo = None):
        super().__init__()
        self.auth = auth
        self.message = message

        # self.db_helper = DBHelper()

        self.client = None
        self.db = None
        self.collection = None

    def initialize_client(self):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        client = None

        try:
            if self.auth:
                authy = self.auth.to_json()

                client = pymongo.MongoClient(authy.get("db_form", ""))
                status = self.client_pre_scrap_actions()

                if status:
                    self.message.db_exists = True
                    self.client = client

                else:
                    self.logger.warning(f"Class {class_name} of method {method_name}: Unable to initialize pre-scrap. "
                                        f"Voiding client session with MongoDB.")
                    client = None

            else:
                self.logger.warning(f"Class {class_name} of method {method_name}: No authentication info given.")

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return client

    def client_pre_scrap_actions(self) -> bool:
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
