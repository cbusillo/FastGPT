from pydantic import BaseModel


class StartConversationRequest(BaseModel):
    model_name: str


class StartConversationResponse(BaseModel):
    conversation_id: str


class Message(BaseModel):
    message: str


class GetConversationResponse(BaseModel):
    messages: list[Message]


class AddMessageRequest(BaseModel):
    message: str
    sender: str


class AddMessageResponse(BaseModel):
    status: str


class EndConversationResponse(BaseModel):
    status: str
