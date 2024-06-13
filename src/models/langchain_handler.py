import inspect
import json
from typing import List

import certifi
import pymongo
from bson import ObjectId
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
# from langchain.chat_models import AzureChatOpenAI
# from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.vectorstores import AzureCosmosDBVectorSearch
from langchain_core.documents import Document
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import Tool, StructuredTool

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
                    #Changed by wyapb
                    # text_key="_id"
                    text_key="id"
                    #end change
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

    def rag_vector_search(self):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = None

        try:
            retriever = self.vector_store.as_retriever()
            llm_prompt = PromptTemplate.from_template(self.message.prompt)

            rag_chain = (
                # populate the tokens/placeholders in the llm_prompt
                # information takes the results of the vector store and formats the documents
                # question is a passthrough that takes the incoming question
                    {"information": retriever | self.format_docs, "question": RunnablePassthrough()} | llm_prompt
                    # pass the populated prompt to the language model
                    | self.client
                    # return the string ouptut from the language model
                    | StrOutputParser()
            )

            result = rag_chain.invoke(self.message.query)

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return result

    def format_docs(self, temp: List[Document]):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = None
        temp_docs = list()

        try:
            for entry in temp:
                # Build the product document without the contentVector
                entry_dict = {"_id": entry.page_content}
                entry_dict.update(entry.metadata)

                if "contentVector" in entry_dict:
                    del entry_dict["contentVector"]

                temp_docs.append(json.dumps(entry_dict, default=str))

            result = "\n\n".join(temp_docs)

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return result

    def create_vector_store_retriever(self):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = None

        try:
            result = self.vector_store.as_retriever(search_kwargs={"k": self.message.k_search_value})

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return result

    def create_agent_tool(self):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = None

        try:
            retriever = self.create_vector_store_retriever()

            retriever_chain = retriever | self.format_docs

            tools = [
                Tool(
                    name=f"vector_search_{self.message.collection_name}",
                    func=retriever_chain.invoke,
                    description=f"Searches {self.message.database_name} {self.message.collection_name} information for "
                                f"similar {self.message.collection_name} based on the question."
                )
            ]

            tools.extend([
                StructuredTool.from_function(self.get_entry_by_id)
            ])

            result = tools

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return result

    def get_entry_by_id(self, product_id: str) -> str:
        """
        Retrieves an entry by its ID.
        :return: str
        """
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = None

        try:
            db_client = pymongo.MongoClient(self.auth.db_form, tlsCAFile=certifi.where())
            db = db_client[f"{self.message.database_name}"]
            collection = db[f"{self.message.collection_name}"]

            doc = collection.find_one({"id": product_id})

            if "contentVector" in doc:
                del doc["contentVector"]

            result = json.dumps(doc)

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return result

    def create_agent(self):
        class_name = self.__class__.__name__
        method_name = inspect.currentframe().f_code.co_name
        result = None

        try:
            system_message = SystemMessage(content=self.message.prompt)
            tools = self.create_agent_tool()

            agent_executor = create_conversational_retrieval_agent(self.client, tools, system_message=system_message,
                                                                   verbose=True)

            result = agent_executor({"input": self.message.query})

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

            elif subtask == SUBTASK_CONST.CREATE_VEC_STORE:
                self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                 f"Declaring sub-task completed.")
                result = self.create_vector_store_retriever()
                self.message.subtask_completed = True

            elif subtask == SUBTASK_CONST.CREATE_AGENT_TOOL:
                self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                 f"Declaring sub-task completed.")
                result = self.create_agent_tool()
                self.message.subtask_completed = True

            elif subtask == SUBTASK_CONST.CREATE_AGENT:
                self.logger.info(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                 f"Declaring sub-task completed.")
                result = self.create_agent()
                self.message.subtask_completed = True

            else:
                self.logger.warning(f"Class {class_name} of method {method_name}: {subtask} determined. "
                                    f"Unable to determine correct sub-tasking. Failing.")
                result = self.create_agent()
                self.message.subtask_completed = True

        except Exception as bad_exception:
            self.logger.error(f"Exception encountered in class {class_name} of method {method_name}: {bad_exception}")

        finally:
            return result
