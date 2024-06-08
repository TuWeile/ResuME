from decorators.decorators import Singleton

@Singleton
class PurposePojo:
    """
    Message delivery POJO object for subtasking and division of missions for application to handle
    """
    def __init__(self):
        self.model: str = "gpt-4"  # FIXME: Replace str with MODEL_CONST class.
        
        self.task: str = ""  # FIXME: Replace str with TASK_CONST class.
        self.subtask: str = ""  # FIXME: Replace str with SUBTASK_CONST || SUBTASK_DB_CONST class.
    
    def to_json(self):
        """
        Generates a JSON / dict output from the PurposePojo attributes.
        :return:  A dict object: a JSON version of the message POJO structure.
        """
        return vars(self)
