from bson.objectid import ObjectId
from datetime import datetime
import unittest

from constants.constants import TASK_CONST, SUBTASK_CONST, MODEL_CONST, SUBTASK_DB_CONST, TEST_PROD_CONST
from helper.common_helper import CommonHelper
from helper.config_helper import ConfigHelper
from helper.file_helper import FileHelper
from helper.logger_helper import LoggerHelper
from pojo.auth_pojo import AuthPojo
from pojo.input_pojo import InputPojo, ReadIdPojo
from pojo.user_pojo import PersonalInfo, User, Address, UserUpdateSearch
from src.app.app_handler import AppHandler


class MyTestCase(unittest.TestCase):
    file_helper = FileHelper()
    common_helper = CommonHelper()
    config_helper = ConfigHelper()
    logger = LoggerHelper()
    message = InputPojo()

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
        id=f"{common_helper.get_id_random()}",
        personal_info=test_personal_info,
        created_at=common_helper.get_current_time(),
        deleted_by=common_helper.get_current_time() + 172800
    )

    config = config_helper.read_ini(file_helper.resolve_path("config.ini", 1))

    def test_connect_to_openai(self):
        """
        This test case verifies the connection to the OpenAI model. It sets up the necessary configuration and role parameters to connect to the OpenAI model and checks whether the task is marked as done. It also ensures that the client_exists flag is set to True, indicating a successful connection.
        """
        authy = AuthPojo(self.config)

        self.message.role.model = MODEL_CONST.GPT4
        self.message.role.task = TASK_CONST.CONNECT
        self.message.role.subtask = SUBTASK_CONST.CLIENT

        self.message.task_completed = False
        self.message.subtask_completed = False

        status = AppHandler(authy, self.message).main()

        if not self.message.done:
            self.fail(f"The task was not completed with self.message.done declared as {self.message.done}")

        self.assertEqual(self.message.client_exists, True, "Connection to OpenAI model flagged as False.")

    def test_create_response(self):
        """
        This test case tests the response creation functionality of the OpenAI model. It sets up the configuration and role parameters to simulate a conversation with predefined messages. The test ensures that the task is marked as done and that the last message received from the model is not empty, indicating a successful response generation.
        """
        authy = AuthPojo(self.config)

        # You might have to change in between MODEL_CONST and TEST_PROD_CONST depending on which provider you are using.
        self.message.role.model = TEST_PROD_CONST.COMPLETIONS
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

        if not self.message.done:
            self.fail(f"The task was not completed with self.message.done declared as {self.message.done}")

        self.logger.debug(f"Response received: {self.message.last_message}")

        self.assertNotEqual(self.message.last_message, "", "No last message received from model.")

    def test_connect_to_mongodb(self):
        """
        This test case verifies the connection to a MongoDB database. It sets up the necessary configuration and role parameters for database connection and checks whether the db_exists flag is set to True, indicating a successful connection to the MongoDB database.
        """
        authy = AuthPojo(self.config)

        self.message.role.model = MODEL_CONST.GPT4
        self.message.role.task = TASK_CONST.DATABASE
        self.message.role.subtask = SUBTASK_CONST.CLIENT

        self.message.task_completed = False
        self.message.subtask_completed = False

        status = AppHandler(authy, self.message).main()
        self.assertEqual(self.message.db_exists, True, "Connection to MongoDB flagged as False.")

    def test_create_document_to_db(self):
        """
        This test case tests the document creation functionality in a MongoDB database. It sets up the necessary configuration, creates a test user with personal information, and attempts to create a document in the database. The test ensures that the task is marked as done and that the returned status is an instance of ObjectId, indicating that a document was successfully created in the database.
        """
        authy = AuthPojo(self.config)

        self.message.documents.append(self.test_user)
        self.message.role.task = TASK_CONST.DATABASE
        self.message.role.subtask = SUBTASK_DB_CONST.CREATE

        self.message.task_completed = False
        self.message.subtask_completed = False

        status = AppHandler(authy, self.message).main()

        if not self.message.done:
            self.fail(f"The task was not completed with self.message.done declared as {self.message.done}")
        
        self.logger.debug(status)

        self.assertIsInstance(status, ObjectId, "Status is not an instance of ObjectId")

    def test_read_document_fro_db(self):
        """
        This test case tests the document reading functionality from a MongoDB database. It sets up the necessary configuration and a test ObjectId to read a document from the database. The test ensures that the task is marked as done and that the returned status is an instance of User, indicating that the document was successfully read from the database.
        """
        authy = AuthPojo(self.config)
        read_obj = ReadIdPojo()

        read_obj._id = ObjectId("6662786b720a7fea8f2df4f1")  # or change this value to something that you can find in your own chromoDB

        self.message.read_ids.append(read_obj)
        self.message.role.task = TASK_CONST.DATABASE
        self.message.role.subtask = SUBTASK_DB_CONST.READ

        self.message.task_completed = False
        self.message.subtask_completed = False

        status = AppHandler(authy, self.message).main()

        if not self.message.done:
            self.fail(f"The task was not completed with self.message.done declared as {self.message.done}")
        
        self.logger.debug(status)

        self.assertIsInstance(status, User, "Status is not an instance of User")

    def test_update_document_to_db(self):
        authy = AuthPojo(self.config)
        read_obj = ReadIdPojo()
        set_obj = read_obj.set.get("$set", {})

        amends = UserUpdateSearch(
            biography="Loves pineapple on pizza."
        )

        read_obj._id = ObjectId("6662786b720a7fea8f2df4f1")
        set_obj.update(amends)
        self.message.read_ids.append(read_obj)

        self.message.role.task = TASK_CONST.DATABASE
        self.message.role.subtask = SUBTASK_DB_CONST.UPDATE

        self.message.task_completed = False
        self.message.subtask_completed = False

        status = AppHandler(authy, self.message).main()

        if not self.message.done:
            self.fail(f"The task was not completed with self.message.done declared as {self.message.done}")
        
        self.logger.debug(status)
        
        self.assertIsInstance(status, User, "Status is not an instance of User")
        

    def test_delete_document_fro_db(self):
        authy = AuthPojo(self.config)
        read_obj = ReadIdPojo()

        read_obj._id = ObjectId("6662786b720a7fea8f2df4f1")  # or change this value to something that you can find in your own chromoDB

        self.message.read_ids.append(read_obj)
        self.message.role.task = TASK_CONST.DATABASE
        self.message.role.subtask = SUBTASK_DB_CONST.DELETE

        self.message.task_completed = False
        self.message.subtask_completed = False

        status = AppHandler(authy, self.message).main()

        if not self.message.done:
            self.fail(f"The task was not completed with self.message.done declared as {self.message.done}")
        
        self.logger.debug(status)
        
        self.assertEquals(status, 1, "delete_doc.deleted_count has given an incorrect number.")

    def test_search_documents_fro_db(self):
        """
        Test case for searching documents from the database based on a filter.
        This test queries documents with a specific biography field value and
        ensures the result is a list of ObjectId instances.
        """

        authy = AuthPojo(self.config)
        read_obj = ReadIdPojo()
        set_obj = read_obj.set.get("$set", {})

        query = UserUpdateSearch(
            biography="Loves pineapple on pizza."
        )

        set_obj.update(query)
        self.message.read_ids.append(read_obj)

        self.message.role.task = TASK_CONST.DATABASE
        self.message.role.subtask = SUBTASK_DB_CONST.FILTER

        self.message.task_completed = False
        self.message.subtask_completed = False

        status = AppHandler(authy, self.message).main()

        if not self.message.done:
            self.fail(f"The task was not completed with self.message.done declared as {self.message.done}")
        
        self.logger.debug(status)
        
        self.assertEqual(len(status), 1, "Not the same exact user count has been identified.")

if __name__ == '__main__':
    unittest.main()
