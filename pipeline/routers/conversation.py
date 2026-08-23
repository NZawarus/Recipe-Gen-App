from fastapi import APIRouter, HTTPException
from models.conversations import Conversation, ConversationCreate, ConversationGet, ConversationUpdate, ConversationDelete, Message
from services.conversation_service import ConversationService

router = APIRouter()

@router.post("/conversations")
async def create_conversation(conversation: ConversationCreate) -> Conversation:
    return ConversationService().create_conversation(conversation)

@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: int) -> Conversation:
    return ConversationService().get_conversation(conversation_id)

@router.put("/conversations/{conversation_id}")
async def update_conversation(conversation_id: int, conversation: ConversationUpdate) -> Conversation:
    return ConversationService().update_conversation(conversation_id, conversation)

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: int) -> Conversation:
    return ConversationService().delete_conversation(conversation_id)

@router.get("/conversations")
async def get_all_conversations() -> list[Conversation]:
    return ConversationService().get_all_conversations()
