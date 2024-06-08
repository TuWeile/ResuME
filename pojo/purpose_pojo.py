from decorators.decorators import Singleton

@Singleton
class PurposePojo:
    """
    Message delivery POJO object for subtasking and division of missions for application to handle
    """
    def __init__(self):
        self.model: str = "gpt-4"
        self.embeddings: str = "text-embedding-ada-002"
        
        self.task: str = ""
        self.subtask: str = ""

        self.flag: str = ""

        # TODO: Must be converted to a stack, to allow for recursive additions. This requires refactoring.
        self.prev_task: str = ""
        self.prev_subtask: str = ""
    
    def to_json(self):
        """
        Generates a JSON / dict output from the PurposePojo attributes.
        :return:  A dict object: a JSON version of the message POJO structure.
        """
        return vars(self)
