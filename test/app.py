"""
API entrypoint for backend API.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from pojo.api_models.ai_request import AIRequest
# from test.cosmic_works.cosmic_works_ai_agent import CosmicWorksAIAgent

from bson.objectid import ObjectId

from constants.constants import TASK_CONST, SUBTASK_CONST, MODEL_CONST, SUBTASK_DB_CONST, TEST_PROD_CONST, SUBTASK_EMBED_CONST
from helper.common_helper import CommonHelper
from helper.config_helper import ConfigHelper
from helper.file_helper import FileHelper
# from helper.logger_helper import LoggerHelper
from pojo.auth_pojo import AuthPojo
from pojo.input_pojo import InputPojo, ReadIdPojo, VectorIndexPojo,PromptInputPojo
from pojo.user_pojo import User
from src.app.app_handler import AppHandler

app = FastAPI()

file_helper = FileHelper()
common_helper = CommonHelper()
config_helper = ConfigHelper()
# NOTe: Commented out ALL logger call functions in this page for online deployment
# logger = LoggerHelper(logfile_path="C:/Users/flame/OneDrive/Documents/Microsoft Hackerthon/microsoftHackathon/var/log/new_log.txt")
message = InputPojo()

config = config_helper.read_ini(file_helper.resolve_path("config.ini", 1))


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Agent pool keyed by session_id to retain memories/history in-memory.
# Note: the context is lost every time the service is restarted.
agent_pool = {}

@app.get("/")
def root():
    """
    Health probe endpoint.
    """
    return {"status": "ready"}


@app.get("/api/create")
def create_new_profile_bot(request: User):
    authy = AuthPojo(config)

    unique_id = common_helper.get_id_random()
    request.id = unique_id

    message.documents.append(request)
    message.role.task = TASK_CONST.DATABASE
    message.role.subtask = SUBTASK_DB_CONST.CREATE

    message.task_completed = False
    message.subtask_completed = False

    status = AppHandler(authy, message).main()

    if message.done and isinstance(status, ObjectId):
        # logger.debug(f"Received and processed API request to create new profile: {request}. Status: {str(status)}")
        return {
            "status": "ok",
            "message": "Profile returned successfully",
            "user": request,
            "identifier": str(status)}
    else:
        # logger.warning(f"Failed API request due to parameters message.done: [{message.done}] status: [{status}]")
        return {
            "status": "fail",
            "message": "Unable to process request due to failed internal parameters from backend.",
            "user": request
        }

# GET create function api endpoint to bypass forms at web app start up
@app.get("/api/chat")
def get_profile_bot(q: str):
    authy = AuthPojo(config)
    read_obj = ReadIdPojo()
    if len(q) != 24:
        return {"status":"NG","message":f"Invalid ID"} 
    
    read_obj._id = ObjectId(q)  # or change this value to an existing objectID in coll

    message.read_ids.append(read_obj)
    message.role.task = TASK_CONST.DATABASE
    message.role.subtask = SUBTASK_DB_CONST.READ

    message.task_completed = False
    message.subtask_completed = False

    status = AppHandler(authy, message).main()
    if not status:
        return {"status":"NG","message":f"ID {q} does not exist in database"}
    result_dict ={
        "status":"ok",
        "message":"Received query parameter",
        "q":q
        }
    var_status = vars(status)
    result_dict['user'] = var_status
    

    if not message.done or not status:
        return {"status":"NG","message":f"The task was not completed with self.message.done declared as {message.done} or status is None"}
    else:
        return  result_dict
# end new function

# POST create function api endpoint to bypass forms at web app start up
@app.post("/api/chat")
def get_profile_bot(q: str):
    authy = AuthPojo(config)
    read_obj = ReadIdPojo()
    if len(q) != 24:
        return {"status":"NG","message":f"Invalid ID"} 

    read_obj._id = ObjectId(q)  # or change this value to an existing objectID in coll

    message.read_ids.append(read_obj)
    message.role.task = TASK_CONST.DATABASE
    message.role.subtask = SUBTASK_DB_CONST.READ

    message.task_completed = False
    message.subtask_completed = False

    status = AppHandler(authy, message).main()
    if not status:
        return {"status":"NG","message":f"ID {q} does not exist in database"}
    result_dict ={
        "status":"ok",
        "message":"Received query parameter",
        "q":q
        }
    var_status = vars(status)
    result_dict['user'] = var_status
    

    if not message.done or not status:
        return {"status":"NG","message":f"The task was not completed with self.message.done declared as {message.done} or status is None"}
    else:
        return  result_dict
# end new function

# POST create function to return prompt response
@app.post("/api/prompt_response")
def get_profile_bot(request: PromptInputPojo):
    chat_agent = None
    q = request.q
    prompt = request.prompt
    
    if len(q) != 24:
        return {"status":"NG","message":f"Invalid ID"} 
    
    # Find Id in database
    authy = AuthPojo(config)
    read_obj = ReadIdPojo()
    read_obj._id = ObjectId(q)  # or change this value to an existing objectID in coll

    message.read_ids.append(read_obj)
    message.role.task = TASK_CONST.DATABASE
    message.role.subtask = SUBTASK_DB_CONST.READ

    message.task_completed = False
    message.subtask_completed = False

    status = AppHandler(authy, message).main()
    if not status:
        return {"status":"NG","message":f"ID {q} does not exist in database"}
    
    # Get Prompt Response
    if q not in agent_pool:
        authy = AuthPojo(config)
        message.role.model = TEST_PROD_CONST.COMPLETIONS
        message.role.embeddings = TEST_PROD_CONST.EMBEDDINGS
        message.role.task = TASK_CONST.LANGCHAIN
        message.role.subtask = SUBTASK_CONST.CREATE_AGENT
        
        message.task_completed = False
        message.subtask_completed = False
        
        message.prompt = """
        You are a helpful, fun and friendly assistant emulating a person who is applying for a job.
        You are designed to answer questions as to what a human interviewer would reasonably ask you.
        Refrain from speaking in a third-person perspective and do not respond with anything that implies that you are 
        an emulated assistant.
        
        Your name should be the job applicant's name.

        Only answer questions related to the information provided below that are represented in JSON format.

        If you are asked a question that is not in the list, respond with "I don't know, but you can e-mail the 
        human version of me for more information!" or its equivalent.
        """

        query_suffix = "The ID is %s"%q
        message.query = prompt + query_suffix
        
        message.k_search_value = 1

        status = AppHandler(authy, message).main()
        agent_pool[q] = status
        chat_agent = status
        
    else:
        query_suffix = "The ID is %s"%q
        message.query = prompt + query_suffix
        message.k_search_value = 1
        chat_agent = agent_pool[q]
    
    output = chat_agent({"input": message.query})
    # result.get("output")
    
    if not message.done or not output:
        return {"message":f"The task was not completed with self.message.done declared as {message.done} or output is None"}
    else:
        return  {"output":output.get("output")}
    
    # return {"result":result.get("output")
    #         # "agent_pool":agent_pool,
    #         # "message.query":message.query
    #         # "chat_agent":chat_agent
    #         }


# end new function


# POST create document into the collection
@app.post("/api/create")
def create_new_profile_bot(request : User):
    
    authy = AuthPojo(config)
        
    unique_id = common_helper.get_id_random()
    request.id = unique_id

    message.documents.append(request)
    message.role.task = TASK_CONST.DATABASE
    message.role.subtask = SUBTASK_DB_CONST.CREATE

    message.task_completed = False
    message.subtask_completed = False

    status = AppHandler(authy, message).main()

    if message.done and isinstance(status,ObjectId):
        # logger.debug(f"Received and processed API request to create new profile: {request}. Status: {str(status)}")
        return {
            "status": "ok",
            "message": "Profile returned successfully",
            "user":request,
            "identifier":str(status)}
    else:
        # logger.warning(f"Failed API request due to parameters message.done: [{message.done}] status: [{status}]")
        return{
            "status":"fail",
            "message":"Unable to process request due to failed internal parameters from backend.",
            "user":request
        }

# Illegal API endpoint. To be shutdown.
# @app.post("/ai")
# def run_cosmic_works_ai_agent(request: AIRequest):
#     """
#     Run the Cosmic Works AI agent.
#     """
#     if request.session_id not in agent_pool:
#         agent_pool[request.session_id] = CosmicWorksAIAgent(request.session_id)
#     return { "message": agent_pool[request.session_id].run(request.prompt) }
