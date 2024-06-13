"""
API entrypoint for backend API.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from pojo.api_models.ai_request import AIRequest
# from test.cosmic_works.cosmic_works_ai_agent import CosmicWorksAIAgent

from bson.objectid import ObjectId

from constants.constants import TASK_CONST, SUBTASK_DB_CONST
from helper.common_helper import CommonHelper
from helper.config_helper import ConfigHelper
from helper.file_helper import FileHelper
from helper.logger_helper import LoggerHelper
from pojo.auth_pojo import AuthPojo
from pojo.input_pojo import InputPojo
from pojo.user_pojo import User
from src.app.app_handler import AppHandler

app = FastAPI()

file_helper = FileHelper()
common_helper = CommonHelper()
config_helper = ConfigHelper()
logger = LoggerHelper(logfile_path="C:/Users/flame/OneDrive/Documents/Microsoft Hackerthon/microsoftHackathon/var/log/new_log.txt")
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
        logger.debug(f"Received and processed API request to create new profile: {request}. Status: {str(status)}")
        return {
            "status": "ok",
            "message": "Profile returned successfully",
            "user":request,
            "identifier":str(status)}
    else:
        logger.warning(f"Failed API request due to parameters message.done: [{message.done}] status: [{status}]")
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
