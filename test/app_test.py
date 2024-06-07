from datetime import datetime
import unittest

from constants.constants import TASK_CONST, SUBTASK_CONST, MODEL_CONST, SUBTASK_DB_CONST
from helper.common_helper import CommonHelper
from helper.config_helper import ConfigHelper
from helper.file_helper import FileHelper
from helper.logger_helper import LoggerHelper
from pojo.auth_pojo import AuthPojo
from pojo.input_pojo import InputPojo
from pojo.user_pojo import PersonalInfo, User, Address
from src.app.app_handler import AppHandler


class MyTestCase(unittest.TestCase):
    file_helper = FileHelper()
    common_helper = CommonHelper()
    config_helper = ConfigHelper()
    logger = LoggerHelper()
    message = InputPojo()

    config = config_helper.read_ini(file_helper.resolve_path("config.ini", 1))

    def test_connect_to_openai(self):
        authy = AuthPojo(self.config)

        self.message.role.model = MODEL_CONST.GPT4
        self.message.role.task = TASK_CONST.CONNECT
        self.message.role.subtask = SUBTASK_CONST.CLIENT

        self.message.task_completed = False
        self.message.subtask_completed = False

        status = AppHandler(authy, self.message).main()

        self.assertEqual(self.message.client_exists, True)

    def test_create_response(self):
        authy = AuthPojo(self.config)

        self.message.role.model = MODEL_CONST.GPT4
        self.message.role.task = TASK_CONST.CONNECT
        self.message.role.subtask = SUBTASK_CONST.RESPONSE

        self.message.messages = [
            {"role": "system",
             "content": "You are a helpful, fun and friendly sales assistant for Cosmic Works, a bicycle and bicycle "
                        "accessories store."},
            {"role": "user", "content": "Do you sell bicycles?"},
            {"role": "assistant", "content": "Yes, we do sell bicycles. What kind of bicycle are you looking for?"},
            {"role": "user", "content": "I'm not sure what I'm looking for. Could you help me decide?"}
        ]

        self.message.task_completed = False
        self.message.subtask_completed = False

        status = AppHandler(authy, self.message).main()
        self.logger.debug(f"Response received: {self.message.last_message}")

        self.assertNotEqual(self.message.last_message, "")

    def test_connect_to_mongodb(self):
        authy = AuthPojo(self.config)

        self.message.role.model = MODEL_CONST.GPT4
        self.message.role.task = TASK_CONST.DATABASE
        self.message.role.subtask = SUBTASK_CONST.CLIENT

        self.message.task_completed = False
        self.message.subtask_completed = False

        status = AppHandler(authy, self.message).main()
        self.assertEqual(self.message.db_exists, True)

    def test_create_document_to_db(self):
        authy = AuthPojo(self.config)

        test_address = Address(
            street="21 Lower Kent Ridge Rd",
            city="Singapore",
            state="Singapore",
            zip="119077",
            country="Singapore"
        )

        test_personal_info = PersonalInfo(
            first_name="John",
            last_name="Doe",
            email="johndoe@test.com",
            phone="91234567",
            address=test_address,
            date_of_birth=f"{datetime(2000, 12, 25)}"
        )

        test_user = User(
            id=f"{self.common_helper.get_id_random()}",
            personal_info=test_personal_info,
            created_at=self.common_helper.get_current_time(),
            deleted_by=self.common_helper.get_current_time() + 172800
        )

        self.message.documents.append(test_user)
        self.message.role.task = TASK_CONST.DATABASE
        self.message.role.subtask = SUBTASK_DB_CONST.CREATE

        self.message.task_completed = False
        self.message.subtask_completed = False

        status = AppHandler(authy, self.message).main()

        self.assertEqual(status, True)

    def test_read_document_fro_db(self):
        pass

    def test_update_document_to_db(self):
        pass

    def test_delete_document_fro_db(self):
        pass

    def test_query_multiple_documents_db(self):
        pass


if __name__ == '__main__':
    unittest.main()
