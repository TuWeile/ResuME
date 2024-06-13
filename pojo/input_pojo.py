from decorators.decorators import Singleton
from pojo.purpose_pojo import PurposePojo

from bson.objectid import ObjectId
from pojo.user_pojo import PersonalInfo, UserUpdateSearch, Address
from pydantic import BaseModel
from typing import List, Optional


@Singleton
class InputPojo:
    """
    Message delivery POJO object for subtasking and delivery of specific values.
    """
    def __init__(self):
        self.messages: list[dict] = [{}]
        self.last_message: str = ""
        self.embed_message: str = ""

        self.prompt: str = ""
        self.query: str = ""
        self.k_search_value: int = 3
        self.chunk_size: int = 32

        self.documents: List[BaseModel] = []
        self.read_ids: List[ReadIdPojo] = []
        self.vector_index: VectorIndexPojo = VectorIndexPojo()

        self.role: PurposePojo = PurposePojo()

        self.task_completed: bool = False
        self.subtask_completed: bool = False
        self.done: bool = False

        self.client_exists: bool = False
        self.db_exists: bool = False
        self.langchain_exists: bool = False

        self.database_name: str = "cosmic_works"
        self.collection_name: str = "products"

    def to_json(self):
        """
        Generates a JSON / dict output from the InputPojo attributes.
        :return:  A dict object: a JSON version of the message POJO structure.
        """
        return vars(self)


@Singleton
class ReadIdPojo:
    """
    Reading ID POJO object for reading IDs from documents
    """
    def __init__(self):
        self._id: ObjectId = ObjectId()
        self.set: Optional[dict[UserUpdateSearch]] = {"$set": {}}
    
    def to_json(self):
        """
        Generates a JSON / dict output from the ReadIdPojo attributes.
        :return:  A dict object: a JSON version of the message POJO structure.
        """
        return vars(self)


class VectorIndexPojo:
    def __init__(self):
        self.createIndexes: str = ""
        self.indexes: List[dict] = [CosmosIndexPojo().to_json()]

    def to_json(self):
        """
        Generates a JSON / dict output from the VectorIndexPojo attributes.
        :return:  A dict object: a JSON version of the message POJO structure.
        """
        return vars(self)


class CosmosIndexPojo:
    def __init__(self):
        self.name: str = "VectorSearchIndex"
        self.key: dict = {"contentVector": "cosmosSearch"}
        self.cosmosSearchOptions: dict = {"kind": "vector-ivf",
                                          "numLists": 1,
                                          "similarity": "COS",
                                          "dimensions": 1536}

    def to_json(self):
        """
        Generates a JSON / dict output from the VectorIndexPojo attributes.
        :return:  A dict object: a JSON version of the message POJO structure.
        """
        return vars(self)
