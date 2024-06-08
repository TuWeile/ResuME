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
        self.documents: List[BaseModel] = []
        self.read_ids : List[ReadIdPojo] = []

        self.role: PurposePojo = PurposePojo()

        self.task_completed: bool = False
        self.subtask_completed: bool = False
        self.done: bool = False

        self.client_exists: bool = False
        self.db_exists: bool = False

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
        self._id: ObjectId = ""
        self.set: Optional[dict[UserUpdateSearch]] = {"$set": {}}
    
    def to_json(self):
        """
        Generates a JSON / dict output from the ReadIdPojo attributes.
        :return:  A dict object: a JSON version of the message POJO structure.
        """
        return vars(self)
