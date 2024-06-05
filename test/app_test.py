import unittest

from helper.config_helper import ConfigHelper
from helper.file_helper import FileHelper
from helper.logger_helper import LoggerHelper
from pojo.auth_pojo import AuthPojo
from pojo.input_pojo import InputPojo
from src.app.app_handler import AppHandler


class MyTestCase(unittest.TestCase):
    file_helper = FileHelper()
    config_helper = ConfigHelper()
    logger = LoggerHelper()
    message = InputPojo()

    config = config_helper.read_ini(file_helper.resolve_path("config.ini", 1))

    def test_connect_to_openai(self):
        authy = AuthPojo(self.config)
        status = AppHandler(authy, self.message).main()

        self.assertEqual(self.message.client_exists, True)  # add assertion here

    def test_create_response(self):
        authy = AuthPojo(self.config)

        self.message.messages = [
            {"role": "system",
             "content": "You are a helpful, fun and friendly sales assistant for Cosmic Works, a bicycle and bicycle "
                        "accessories store."},
            {"role": "user", "content": "Do you sell bicycles?"},
            {"role": "assistant", "content": "Yes, we do sell bicycles. What kind of bicycle are you looking for?"},
            {"role": "user", "content": "I'm not sure what I'm looking for. Could you help me decide?"}
        ]

        status = AppHandler(authy, self.message).main()
        self.logger.debug(f"Response received: {self.message.last_message}")

        self.assertNotEqual(self.message.last_message, "")


if __name__ == '__main__':
    unittest.main()
