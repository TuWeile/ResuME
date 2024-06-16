import inspect
import json

import pymongo
from bson import ObjectId

from decorators.decorators import Singleton

from helper.common_helper import CommonHelper
from helper.logger_helper import LoggerHelper

from pojo.input_pojo import ReadIdPojo, VectorIndexPojo
from pojo.user_pojo import User
from pydantic import BaseModel
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from typing import Type, List

from src.models.model_handler import ModelHandler


@Singleton
class DBHelper:
    def __init__(self, client: MongoClient = None, db: Database = None, collection: Collection = None) -> None:
        self.client = client
        self.db = db
        self.collection = collection

        self.logger = LoggerHelper()
        self.helper = CommonHelper()
    
    def create_one_document(self, instance: List[Type[BaseModel]]):
        """
        One method of creating a document is using the insert_one method. This method takes a single document and 
        inserts it into the database. This operation returns an InsertOneResult object that contains the property 
        inserted_id. This property contains the unique identifier of the document that was just inserted.
        """
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
            print("instance_id",instance_id)
            return instance_id

    def read_one_document(self, read: List[ReadIdPojo]):
        """
        The insertion of the Product in the previous cell automatically created the database and collection. The 
        find_one method is used to retrieve a single document from the database. The find_one method takes a 
        filter as an argument. This filter is used to find the document in the database. In this case, the filter 
        is the unique identifier or _id of the document that was just inserted.
        """
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = None

        try:
            if len(read) > 1:
                self.logger.info(f"Class {class_name} of method {method_name}: Taking the latest entry as document.")
                read = read.pop().to_json()
                #Added by wyapb
                read = read['_id']
                #end add

            elif len(read) == 1:
                read = read[0].to_json()
                #Added by wyapb
                read = read['_id']
                #end add

            else:
                raise Exception("Empty read object given.")
            
            retrieved_doc = self.collection.find_one(read)
            
            if not retrieved_doc:
                return None
            
            if retrieved_doc:
                self.logger.info(f"Class {class_name} of method {method_name}: Successfully retrieved document from "
                                 f"ID {read}.")  # FIXME: preferably to include ID in the future.
                result = User(**retrieved_doc)
            
            else:
                self.logger.warning(f"Class {class_name} of method {method_name}: Unable to find retrieved doc.")
        
        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: "
                              f"{bad_exception}")

        finally:
            return result
    
    def update_one_document(self, read: List[ReadIdPojo]):
        """
        The find_one_and_update method is used to update a single document in the database. This method takes a filter and an update as arguments. The filter is used to find the document to update. The update is a dictionary of the properties to update. In this case, the find_one_and_update method is used to update the name property of the document. The updated document is the return value for this method.
        """
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = None

        try:
            if read:
                entry = read[-1]

                entry.set["$set"] = self.helper.dict_remove_null_values(entry.set.get("$set"))
                update_doc = self.collection.find_one_and_update({"_id": entry._id}, entry.set, return_document=pymongo.ReturnDocument.AFTER)
            
                if update_doc:
                    self.logger.info(f"Class {class_name} of method {method_name}: Successfully updated document with parameters for {entry._id}.") 
                    result = User(**update_doc)

                else:
                    self.logger.warning(f"Class {class_name} of method {method_name}: Unable to find updated doc.")
        
        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: "
                              f"{bad_exception}")

        finally:
            return result
    
    def delete_one_document(self, read: List[ReadIdPojo]):
        """
        The delete_one method is used to delete a single document from the database. This method takes a filter as an argument. This filter is used to find the document to delete. In this case, the filter is the unique identifier or _id of the document that was just inserted and updated.
        """
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = None

        try:
            if read:
                entry = read[-1]

                delete_doc = self.collection.delete_one({"_id": entry._id})

                if delete_doc.acknowledged:
                    self.logger.info(f"Class {class_name} of method {method_name}: Successfully deleted document with parameters ID {entry}.")
                    self.logger.debug(f"Deleted documents count: {delete_doc.deleted_count} | Number of docs left: {self.count_all_documents()}") 
                    result = delete_doc.deleted_count

                else:
                    self.logger.warning(f"Class {class_name} of method {method_name}: Unable to find updated doc.")
        
        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: "
                              f"{bad_exception}")

        finally:
            return result
    
    def find_documents(self, read: List[ReadIdPojo]):
        """
        The find method is used to query for multiple documents in the database. This method takes a filter as an argument. This filter is used to find the documents to return. In this case, the filter is an empty dictionary. This will return all documents in the collection.
        """
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = list()
        
        try:
            if read:
                entry = read[-1]
                entry.set["$set"] = self.helper.dict_remove_null_values(entry.set.get("$set"))

                for document in self.collection.find(entry.set["$set"]):
                    result.append(document)
                
                if result:
                    self.logger.info(f"Class {class_name} of method {method_name}: Successfully queried database with query {entry.set}.")
                
                else:
                    self.logger.info(f"Class {class_name} of method {method_name}: No result found from query {entry.set}.")

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: "
                              f"{bad_exception}")

        finally:
            return result

    def count_all_documents(self):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        
        try:
            return self.collection.count_documents({})
        
        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: "
                              f"{bad_exception}")

    def vectorize_and_update_documents(self, client: ModelHandler = None):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = False
        temp = list()

        try:
            if client:
                for doc in self.collection.find():
                    # Remove any previous contentVector embeddings
                    if "contentVector" in doc:
                        del doc["contentVector"]

                    content = json.dumps(doc, default=str)
                    content_vector = client.generate_embeddings(message=content)

                    read = ReadIdPojo()
                    read._id = ObjectId(doc["_id"])
                    read.set["$set"] = {"contentVector": content_vector}

                    temp.append(pymongo.UpdateOne({"_id": read._id}, read.set, upsert=True))

                self.collection.bulk_write(temp)
                result = True

            else:
                self.logger.warning(f"Class {class_name} of method {method_name}: Unable to obtain client.")

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: "
                              f"{bad_exception}")

        finally:
            return result

    def create_vector_index(self, vector_index: VectorIndexPojo = None):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = False

        try:
            if vector_index:
                entry = vector_index.to_json()

                self.db.command(entry)
                result = True

            else:
                self.logger.warning(f"Class {class_name} of method {method_name}: Vector index is empty.")

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: "
                              f"{bad_exception}")

        finally:
            return result

    def vector_search(self, client: ModelHandler = None, query: str = "", num_results: int = 3):
        """
        Perform a vector search on the specified collection by vectorizing
        the query and searching the vector index for the most similar documents.

        returns a list of the top num_results most similar documents
        """
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = None

        try:
            if client and query:
                query_embedding = client.generate_embeddings(message=query)

                # FIXME: Could be better phrased into a POJO class in input_pojo.py.
                pipeline = [
                    {
                        '$search': {
                            "cosmosSearch": {
                                "vector": query_embedding,
                                "path": "contentVector",
                                "k": num_results
                            },
                            "returnStoredSource": True}},
                    {'$project': {'similarityScore': {'$meta': 'searchScore'}, 'document': '$$ROOT'}}
                ]

                result = self.collection.aggregate(pipeline)
                #Added by wyapb , result now returns a of top num_results similarity searches
                # result = result._CommandCursor__data
                ##End add

            elif not client:
                self.logger.warning(f"Class {class_name} of method {method_name}: Unable to obtain client.")

            elif not query:
                self.logger.warning(f"Class {class_name} of method {method_name}: Empty query.")

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: "
                              f"{bad_exception}")

        finally:
            return result

