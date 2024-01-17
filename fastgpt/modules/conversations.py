# conversations.py
from datetime import datetime

from pydantic import BaseModel, Field
from uuid import uuid4


class Message(BaseModel):
    role: str
    content: str
    model: str
    timestamp: datetime = Field(default_factory=datetime.now)


class Conversation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    messages: list[Message] = []
