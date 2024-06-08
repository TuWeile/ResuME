from enum import Enum, auto


class TASK_CONST(Enum):
    CONNECT = auto()
    DATABASE = auto()


class SUBTASK_CONST(Enum):
    CLIENT = auto()
    RESPONSE = auto()


class SUBTASK_DB_CONST(Enum):
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()
    FILTER = auto()


class MODEL_CONST(Enum):
    GPT4 = "gpt-4"
    GPT35_TURBO = "gpt-35-turbo"


class TEST_PROD_CONST(Enum):
    COMPLETIONS = "completions"
    EMBEDDINGS = "embeddings"
