from decorators.decorators import Singleton

@Singleton
class PurposePojo:
    """
    Message delivery POJO object for subtasking and division of missions for application to handle
    """
    def __init__(self):
        self.model: str = "gpt-4"
        
        self.task: str = ""
        self.subtask: str = ""
    
    def to_json(self):
        """
        Generates a JSON / dict output from the PurposePojo attributes.
        :return:  A dict object: a JSON version of the message POJO structure.
        """
        return vars(self)
