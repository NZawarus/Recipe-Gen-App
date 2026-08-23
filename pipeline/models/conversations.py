from pydantic import BaseModel
from datetime import datetime

class Conversation(BaseModel):
    conversation_id: int
    user_id: int
    created_at: datetime

class ConversationCreate(BaseModel):
    user_id: int

class ConversationGet(BaseModel):
    conversation_id: int | None = None
    user_id: int | None = None
    created_at: datetime | None = None

class ConversationUpdate(BaseModel):
    user_id: int | None = None

class ConversationDelete(BaseModel):
    conversation_id: int

class Message(BaseModel):
    message_id: int
    conversation_id: int
    sender: str
    message: str
    time_sent: datetime

class MessageCreate(BaseModel):
    conversation_id: int
    sender: str
    message: str

class MessageGet(BaseModel):
    message_id: int | None = None
    conversation_id: int | None = None
    sender: str | None = None
    message: str | None = None
    time_sent: datetime | None = None

class MessageUpdate(BaseModel):
    conversation_id: int | None = None
    sender: str | None = None
    message: str | None = None

class MessageDelete(BaseModel):
    message_id: int

