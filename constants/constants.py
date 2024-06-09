from enum import Enum, auto


class TASK_CONST(Enum):
    CONNECT = auto()
    DATABASE = auto()
    LANGCHAIN = auto()


class SUBTASK_CONST(Enum):
    CLIENT = auto()
    RESPONSE = auto()
    RESPONSE_CONTEXT = auto()
    CREATE_VEC_STORE = auto()
    CREATE_AGENT = auto()
    CREATE_AGENT_TOOL = auto()


class SUBTASK_DB_CONST(Enum):
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()
    FILTER = auto()


class SUBTASK_EMBED_CONST(Enum):
    GENERATE = auto()
    VECTORIZE_UPDATE = auto()
    CREATE_INDEX = auto()
    SEARCH = auto()


class MODEL_CONST(Enum):
    GPT4 = "gpt-4"
    GPT35_TURBO = "gpt-35-turbo"


class TEST_PROD_CONST(Enum):
    COMPLETIONS = "completions"
    EMBEDDINGS = "embeddings"


class FLAG_CONST(Enum):
    INIT_CLIENT = auto()
    INIT_DATABASE = auto()
