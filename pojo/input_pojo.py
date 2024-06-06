from decorators.decorators import Singleton
from pojo.purpose_pojo import PurposePojo

from pydantic import BaseModel
from typing import List


@Singleton
class InputPojo:
    """
    Message delivery POJO object for subtasking and delivery of specific values.
    """
    def __init__(self):
        self.messages: list[dict] = [{}]
        self.last_message: str = ""
        self.documents: List[BaseModel] = []

        self.role: PurposePojo = PurposePojo()

        self.task_completed: bool = False
        self.subtask_completed: bool = False

        self.client_exists: bool = False
        self.db_exists: bool = False

    def to_json(self):
        """
        Generates a JSON / dict output from the InputPojo attributes.
        :return:  A dict object: a JSON version of the message POJO structure.
        """
        return vars(self)
