import inspect

from decorators.decorators import Singleton

from helper.logger_helper import LoggerHelper

from pydantic import BaseModel
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from typing import Type, List


@Singleton
class DBHelper:
    def __init__(self, client: MongoClient = None, db: Database = None, collection: Collection = None) -> None:
        self.client = client
        self.db = db
        self.collection = collection

        self.logger = LoggerHelper()
    
    def create_one_document(self, instance: List[Type[BaseModel]]):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        instance_id = None
        status = None

        try:
            if len(instance) > 1:
                self.logger.info(f"Class {class_name} of method {method_name}: Taking the latest entry as document.")
                instance = instance.pop()

            elif len(instance) == 1:
                instance = instance[0]

            else:
                raise Exception("Empty instance given.")

            # Generate JSON using alias names defined on the model
            instance_json = instance.model_dump(by_alias=True)
            
            # Insert the JSON into the database, and retrieve the inserted/generated ID
            instance_obj = self.collection.insert_one(instance_json)
            instance_id = instance_obj.inserted_id
            status = instance_obj.acknowledged

            if status:
                self.logger.info(f"Class {class_name} of method {method_name}: Successfully created document with "
                                 f"status {status} and inserted to database with ID {instance_id}")

            else:
                self.logger.warning(f"Class {class_name} of method {method_name}: Unintended status {status} "
                                    f"encountered.")
        
        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: "
                              f"{bad_exception}")

        finally:
            return instance_id
