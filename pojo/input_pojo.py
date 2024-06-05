from decorators.decorators import Singleton


@Singleton
class InputPojo:
    """
    Message delivery POJO object for subtasking and delivery of specific values.
    """
    def __init__(self):
        self.model: str = "gpt-4"
        self.messages: list[dict] = [{}]

        self.client_exists: bool = False
        self.last_message: str = ""

    def to_json(self):
        """
        Generates a JSON / dict output from the AuthPojo attributes.
        :return:  A dict object: a JSON version of the message POJO structure.
        """
        return vars(self)
