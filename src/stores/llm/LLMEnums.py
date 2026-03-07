from enum import Enum

class LLMEnums(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"


class OpenAIEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class CohereEnums(Enum):
    DOCUMENT = "search_document"
    QUERY = "search_query"
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "chatbot"


class DocumentTypeEnum(Enum):
    DOCUMENT = "document"
    QUERY = "query" 
    