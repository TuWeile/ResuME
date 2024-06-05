from configparser import ConfigParser

from helper.config_helper import ConfigHelper


class AuthPojo:
    """
    Authentication POJO object for handling of environment or system variables. Used for initialization.
    """
    config_helper = ConfigHelper()

    def __init__(self, config: ConfigParser):
        if not self.config_helper.config and config:
            self.config_helper = ConfigHelper(config)

        if self.config_helper.config:
            self.openai_key = self.config_helper.get_value("AOAI_KEY") or None
            self.endpoint = self.config_helper.get_value("AOAI_ENDPOINT") or None
            self.api_version = self.config_helper.get_value("API_VERSION") or None
            self.standalone = True

    def to_json(self):
        """
        Generates a JSON / dict output from the AuthPojo attributes.
        :return:  A dict object: a JSON version of the message POJO structure.
        """
        return vars(self)
