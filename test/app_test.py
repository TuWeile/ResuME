from bson.objectid import ObjectId
from datetime import datetime
import unittest

from openai.types.chat import ChatCompletion
from pymongo.command_cursor import CommandCursor

from constants.constants import TASK_CONST, SUBTASK_CONST, MODEL_CONST, SUBTASK_DB_CONST, TEST_PROD_CONST, \
    SUBTASK_EMBED_CONST
from helper.common_helper import CommonHelper
from helper.config_helper import ConfigHelper
from helper.file_helper import FileHelper
from helper.logger_helper import LoggerHelper
from pojo.auth_pojo import AuthPojo
from pojo.input_pojo import InputPojo, ReadIdPojo, VectorIndexPojo
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
        Tests the OpenAI model connection process.

        Steps:
        - Initializes the authentication object.
        - Configures the message object to use the GPT-4 model and sets up the task and subtask for connecting to the
        client.
        - Executes the connection process and checks if the task completes successfully.
        - Asserts that the `client_exists` flag is set to True, verifying a successful connection.

        Asserts:
        - The task is marked as completed.
        - A successful connection is confirmed by the `client_exists` flag being True.
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
        Tests the response generation functionality of the configured model.

        Steps:
        - Initializes the authentication object.
        - Sets up predefined messages for a simulated conversation flow in the message object.
        - Configures the task for generating a response and checks if it completes successfully.
        - Verifies that the last message received from the model is not empty, indicating that a response was generated.

        Asserts:
        - The task is marked as completed.
        - The last message from the model is not empty, confirming response generation.
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
        Tests the MongoDB database connection process.

        Steps:
        - Initializes the authentication object.
        - Configures the message object for a database connection task and executes the connection process.
        - Checks if the task completes and verifies that the `db_exists` flag is set to True, indicating a successful
        connection.

        Asserts:
        - The task is marked as completed.
        - A successful connection is confirmed by the `db_exists` flag being True.
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
        Tests the document creation functionality in a MongoDB database.

        Steps:
        - Initializes the authentication object and appends a test user document to the message.
        - Configures and executes the document creation task in the database.
        - Checks if the task completes and verifies that the returned status is an instance of ObjectId, confirming
        document creation.

        Asserts:
        - The task is marked as completed.
        - The returned status is an instance of ObjectId, indicating successful document creation.
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
        Tests the document reading functionality from a MongoDB database.

        Steps:
        - Initializes the authentication object and sets up the ID for the document to be read.
        - Configures and executes the task to read a document from the database.
        - Checks if the task completes and verifies that the returned status is an instance of User, confirming
        successful document retrieval.

        Asserts:
        - The task is marked as completed.
        - The returned status is an instance of User, indicating successful document retrieval.
        """

        authy = AuthPojo(self.config)
        read_obj = ReadIdPojo()

        read_obj._id = ObjectId("6662786b720a7fea8f2df4f1")  # or change this value to an existing objectID in coll

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
        """
        Test the update functionality of a document within the database.

        Steps:
        1. Initialize authentication and document identification objects.
        2. Specify the document ID and the update to be applied (biography updated to "Loves pineapple on pizza").
        3. Configure the message object for a database update operation, setting task and subtask identifiers.
        4. Execute the update using AppHandler and verify that the task completes.
        5. Confirm that the result is an instance of the expected `User` class, indicating a successful update.

        Asserts:
        - Task completion is successful.
        - The returned status is an instance of `User`.
        """

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
        """
        Test the delete functionality for removing a document from the database.

        Steps:
        1. Initialize authentication and set the specific document ID for deletion.
        2. Configure the message object to indicate a database deletion task.
        3. Execute the deletion using AppHandler and ensure the task completes.
        4. Verify that the deletion process returns a status indicating the expected number of documents deleted.

        Asserts:
        - Task completion is verified.
        - The deletion status equals `1`, confirming the correct count of documents deleted.
        """

        authy = AuthPojo(self.config)
        read_obj = ReadIdPojo()

        read_obj._id = ObjectId("6662786b720a7fea8f2df4f1")  # or change this value to something in ur collection

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
        Tests the document search functionality within the database based on specific criteria.

        Steps:
        - Initializes authentication and sets up a query object with a predefined biography field.
        - Appends the query to the message object and configures the task and subtask for database filtering.
        - Executes the search task and checks for successful completion.
        - Verifies that the returned status is a list containing the expected number of ObjectId instances.

        Asserts:
        - The task is marked as completed.
        - The result contains exactly one ObjectId instance, indicating the precise retrieval of matching documents.
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

    def test_generate_embeddings(self):
        """
        Tests the embedding generation for a given message using the configured model.

        Steps:
        - Initializes authentication and sets the message to be embedded.
        - Configures the task for embedding generation and executes it.
        - Checks if the task completes successfully and verifies that the returned embeddings are in a list format.

        Asserts:
        - The task is marked as completed.
        - The embeddings are returned as a list, confirming successful generation.
        """

        authy = AuthPojo(self.config)

        self.message.embed_message = "Hello world!"

        self.message.role.emebddings = TEST_PROD_CONST.EMBEDDINGS
        self.message.role.task = TASK_CONST.CONNECT
        self.message.role.subtask = SUBTASK_EMBED_CONST.GENERATE

        self.message.task_completed = False
        self.message.subtask_completed = False

        status = AppHandler(authy, self.message).main()

        if not self.message.done:
            self.fail(f"The task was not completed with self.message.done declared as {self.message.done}")

        self.logger.debug(status)

        if status:
            self.assertIsInstance(status, list, "Embeddings received is not in list.")

        else:
            self.fail(f"Status fails true condition, value is {status}")

    def test_vectorize_and_update_db(self):
        """
        Tests the functionality of vectorizing data and updating documents in the database accordingly.

        Steps:
        - Initializes authentication and configures the task for vectorizing data and updating the database.
        - Executes the task and checks for successful completion.
        - Verifies that the status returned is a boolean, indicating the success of the update operation.

        Asserts:
        - The task is marked as completed.
        - The returned status is a boolean, confirming successful database update.
        """

        authy = AuthPojo(self.config)

        self.message.role.embeddings = TEST_PROD_CONST.EMBEDDINGS
        self.message.role.task = TASK_CONST.DATABASE
        self.message.role.subtask = SUBTASK_EMBED_CONST.VECTORIZE_UPDATE

        self.message.task_completed = False
        self.message.subtask_completed = False

        status = AppHandler(authy, self.message).main()

        if not self.message.done:
            self.fail(f"The task was not completed with self.message.done declared as {self.message.done}")

        if status:
            self.assertIsInstance(status, bool, f"Status is not a boolean, but is rather {status}.")

        else:
            self.fail(f"Status fails true condition, value is {status}")

    def test_create_vector_index_db(self):
        """
        Tests the creation of a vector index in the database.

        Steps:
        - Initializes authentication and configures the task for creating a vector index in the specified collection.
        - Executes the task and checks for successful completion.
        - Verifies that the status returned is a boolean, indicating the successful creation of the vector index.

        Asserts:
        - The task is marked as completed.
        - The returned status is a boolean, confirming the successful index creation.
        """

        authy = AuthPojo(self.config)

        self.message.role.task = TASK_CONST.DATABASE
        self.message.role.subtask = SUBTASK_EMBED_CONST.CREATE_INDEX

        self.message.vector_index = VectorIndexPojo()
        self.message.vector_index.createIndexes = self.message.collection_name

        self.message.task_completed = False
        self.message.subtask_completed = False

        status = AppHandler(authy, self.message).main()

        if not self.message.done:
            self.fail(f"The task was not completed with self.message.done declared as {self.message.done}")

        if status:
            self.assertIsInstance(status, bool, f"Status is not a boolean, but is rather {status}.")

        else:
            self.fail(f"Status fails true condition, value is {status}")

    def test_vector_search(self):
        """
        Tests the vector search functionality within the database.

        Steps:
        - Initializes authentication and sets up a vector search query and the number of results expected.
        - Configures the task for conducting a vector search and executes it.
        - Checks if the task completes successfully and verifies that the returned cursor matches the expected type.

        Asserts:
        - The task is marked as completed.
        - The status is a CommandCursor, indicating successful execution of the vector search.
        """

        authy = AuthPojo(self.config)

        self.message.role.embeddings = TEST_PROD_CONST.EMBEDDINGS
        self.message.role.task = TASK_CONST.DATABASE
        self.message.role.subtask = SUBTASK_EMBED_CONST.SEARCH

        self.message.query = "What do you like?"
        self.message.k_search_value = 3

        self.message.task_completed = False
        self.message.subtask_completed = False

        status = AppHandler(authy, self.message).main()

        if not self.message.done:
            self.fail(f"The task was not completed with self.message.done declared as {self.message.done}")

        self.logger.debug(status)

        # FIXME: status is giving output ObjectIds as a whole. This is bad. Severe reformatting is needed.

        if status:
            self.assertIsInstance(status, CommandCursor, "Embeddings received is not an instance of CommandCursor.")

        else:
            self.fail(f"Status fails true condition, value is {status}")

    def test_create_response_with_context(self):
        """
        Tests the functionality of generating a context-aware response from the configured model, simulating a job
        application scenario.

        Steps:
        - Initializes the authentication object and configures the messaging parameters to simulate a response
        generation task. The role is set to handle both completions and embeddings, with a specific subtask to
        generate a context-aware response.
        - Sets a complex prompt designed to make the assistant act like a job applicant, answering interview questions
        directly without acknowledging its artificial nature. The prompt includes instructions to respond with a
        default message if the query is out of scope.
        - Executes the task with a query asking "Tell me about yourself." and checks for successful completion.
        - Verifies that the returned status is an instance of `ChatCompletion`, ensuring that the response is
        appropriately generated according to the context set in the prompt.

        Asserts:
        - The task is marked as completed.
        - The status is an instance of `ChatCompletion`, confirming that the response aligns with the requirements of
        the context-aware setup.
        - The response text is logged for debugging purposes.
        """

        authy = AuthPojo(self.config)

        self.message.role.model = TEST_PROD_CONST.COMPLETIONS
        self.message.role.embeddings = TEST_PROD_CONST.EMBEDDINGS
        self.message.role.task = TASK_CONST.CONNECT
        self.message.role.subtask = SUBTASK_CONST.RESPONSE_CONTEXT

        self.message.prompt = """
        You are a helpful, fun and friendly assistant emulating a person who is applying for a job.
        You are designed to answer questions as to what a human interviewer would reasonably ask you.
        Refrain from speaking in a third-person perspective and do not respond with anything that implies that you are 
        an emulated assistant.
        
        Only answer questions related to the information provided below that are represented in JSON format.
        
        If you are asked a question that is not in the list, respond with "I don't know, but you can e-mail the 
        human version of me for more information!" or its equivalent.
        
        Information:
        """

        self.message.query = "Tell me about yourself."
        self.message.k_search_value = 3

        self.message.task_completed = False
        self.message.subtask_completed = False

        status = AppHandler(authy, self.message).main()

        if not self.message.done:
            self.fail(f"The task was not completed with self.message.done declared as {self.message.done}")

        self.logger.debug(status)
        self.logger.debug(self.message.last_message)

        if status:
            self.assertIsInstance(status, ChatCompletion, "Status received is not an instance of ChatCompletion.")

        else:
            self.fail(f"Status fails true condition, value is {status}")

    def test_connect_to_langchain(self):
        authy = AuthPojo(self.config)

        self.message.role.model = TEST_PROD_CONST.COMPLETIONS
        self.message.role.embeddings = TEST_PROD_CONST.EMBEDDINGS
        self.message.role.task = TASK_CONST.LANGCHAIN
        self.message.role.subtask = SUBTASK_CONST.CLIENT

        self.message.task_completed = False
        self.message.subtask_completed = False

        status = AppHandler(authy, self.message).main()

        if not self.message.done:
            self.fail(f"The task was not completed with self.message.done declared as {self.message.done}")

        self.assertEqual(self.message.langchain_exists, True, "Connection to LangChain model flagged as False.")

    def test_connect_to_langchain_vector_store(self):
        authy = AuthPojo(self.config)

        self.message.role.model = TEST_PROD_CONST.COMPLETIONS
        self.message.role.embeddings = TEST_PROD_CONST.EMBEDDINGS
        self.message.role.task = TASK_CONST.LANGCHAIN
        self.message.role.subtask = SUBTASK_EMBED_CONST.SEARCH

        self.message.task_completed = False
        self.message.subtask_completed = False

        self.message.query = "Introduce yourself."
        self.message.k_search_value = 3

        status = AppHandler(authy, self.message).main()

        if not self.message.done:
            self.fail(f"The task was not completed with self.message.done declared as {self.message.done}")

        if status:
            self.assertIsInstance(status, list, "Embeddings received is not in list.")

        else:
            self.fail(f"Status fails true condition, value is {status}")

    def test_create_response_with_context_langchain(self):
        authy = AuthPojo(self.config)

        self.message.role.model = TEST_PROD_CONST.COMPLETIONS
        self.message.role.embeddings = TEST_PROD_CONST.EMBEDDINGS
        self.message.role.task = TASK_CONST.LANGCHAIN
        self.message.role.subtask = SUBTASK_CONST.RESPONSE_CONTEXT

        self.message.task_completed = False
        self.message.subtask_completed = False

        self.message.prompt = """
        You are a helpful, fun and friendly assistant emulating a person who is applying for a job.
        You are designed to answer questions as to what a human interviewer would reasonably ask you.
        Refrain from speaking in a third-person perspective and do not respond with anything that implies that you are 
        an emulated assistant.

        Only answer questions related to the information provided below that are represented in JSON format.

        If you are asked a question that is not in the list, respond with "I don't know, but you can e-mail the 
        human version of me for more information!" or its equivalent.

        Information:
        """

        self.message.query = "Introduce yourself while telling me your address."
        self.message.k_search_value = 3

        status = AppHandler(authy, self.message).main()

        if not self.message.done:
            self.fail(f"The task was not completed with self.message.done declared as {self.message.done}")


if __name__ == '__main__':
    unittest.main()
