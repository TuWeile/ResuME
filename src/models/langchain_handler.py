import inspect

from bson import ObjectId
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.vectorstores import AzureCosmosDBVectorSearch

from constants.constants import SUBTASK_CONST, SUBTASK_EMBED_CONST
from pojo.auth_pojo import AuthPojo
from pojo.input_pojo import InputPojo
from src.app.base_handler import BaseHandler


class LangchainHandler(BaseHandler):

    def __init__(self, auth: AuthPojo = None, message: InputPojo = None):
        super().__init__()
        self.auth = auth
        self.message = message

        self.client = None
        self.embeddings = None
        self.vector_store = None

    def initialize_client(self):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        client = None

        try:
            if self.auth:

                client = AzureChatOpenAI(
                    temperature=0,
                    openai_api_version=self.auth.api_version,
                    azure_endpoint=self.auth.endpoint,
                    openai_api_key=self.auth.openai_key,
                    azure_deployment=self.message.role.model.value
                )

                embedding_model = AzureOpenAIEmbeddings(
                    openai_api_version=self.auth.api_version,
                    azure_endpoint=self.auth.endpoint,
                    openai_api_key=self.auth.openai_key,
                    azure_deployment=self.message.role.embeddings.value,
                    chunk_size=self.message.chunk_size
                )

                vector_store = AzureCosmosDBVectorSearch.from_connection_string(
                    connection_string=self.auth.db_form,
                    namespace=f"{self.message.database_name}.{self.message.collection_name}",
                    embedding=embedding_model,
                    index_name="VectorSearchIndex",
                    embedding_key="contentVector",
                    text_key="_id"
                )

                self.message.langchain_exists = True
                self.message.task_completed = True

                self.client = client
                self.embeddings = embedding_model
                self.vector_store = vector_store

            else:
                self.logger.warning("No authentication keys or information received. Cannot initialize client.")

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return client

    def vector_search(self):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = None

        try:
            if self.auth:
                if not self.vector_store:
                    vector_store = AzureCosmosDBVectorSearch.from_connection_string(
                        connection_string=self.auth.db_form,
                        namespace=f"{self.message.database_name}.{self.message.collection_name}",
                        embedding=self.embeddings,
                        index_name="VectorSearchIndex",
                        embedding_key="contentVector",
                        text_key="_id"
                    )

                    self.vector_store = vector_store

                if self.message.query:
                    result = self.vector_store.similarity_search(
                        query=self.message.query,
                        k=self.message.k_search_value
                    )
                    if result:
                        self.logger.debug("Formatting required due to poor Langchain library functionalities.")
                        result[0].page_content = ObjectId(result[0].page_content)

                    else:
                        self.logger.warning("No results received.")

                else:
                    self.logger.warning("Empty query received.")

            else:
                self.logger.warning("No authentication keys or information received. Cannot initialize client.")

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return result

    def main(self, attachments=None):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = None

        try:
            subtask = self.message.role.subtask

            if subtask == SUBTASK_CONST.CLIENT:
                if self.client:
                    self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                     f"Declaring sub-task completed.")
                    self.message.subtask_completed = True

            elif subtask == SUBTASK_EMBED_CONST.SEARCH:
                self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                 f"Declaring sub-task completed.")
                result = self.vector_search()
                self.message.subtask_completed = True

            elif subtask == SUBTASK_CONST.RESPONSE_CONTEXT:
                self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                f"Declaring sub-task completed.")
                result = self.rag_vector_search()
                self.message.subtask_completed = True

            else:
                self.logger.warning(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                    f"Unable to determine correct sub-tasking. Failing.")
                self.message.subtask_completed = True

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return result
