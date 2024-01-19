# routes/conversations.py
from fastapi import APIRouter, HTTPException

from components.logger import setup_logger
from fastgpt.database.models.conversations import Conversation, Message
from .schemas import *

router = APIRouter()
logger = setup_logger()


@router.post("/conversations", response_model=StartConversationResponse)
async def start_conversation(request: StartConversationRequest) -> StartConversationResponse:
    logger.info("Starting conversation")
    try:
        conversation = await Conversation.create(model_name=request.model_name)
        return StartConversationResponse(conversation_id=str(conversation.id))
    except Exception as e:
        raise HTTPException(
            status_code=400, detail={"error": str(e), "model_name": request.model_name}
        )


@router.get("/conversations/{conversation_id}", response_model=GetConversationResponse)
async def get_conversation(conversation_id: str) -> GetConversationResponse:
    conversation = await Conversation.get_or_none(id=conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = await conversation.messages.all()
    return GetConversationResponse(messages=[Message(message=message.message) for message in messages])


@router.post("/conversations/{conversation_id}/messages", response_model=AddMessageResponse)
async def add_message(
    conversation_id: str, request: AddMessageRequest
) -> AddMessageResponse:
    conversation = await Conversation.get_or_none(id=conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    message = await Message.create(
        conversation_id=conversation_id, sender=request.sender, message=request.message
    )
    return AddMessageResponse(status="Message added")


@router.delete("/conversations/{conversation_id}", response_model=EndConversationResponse)
async def end_conversation(conversation_id: str) -> EndConversationResponse:
    conversation = await Conversation.get_or_none(id=conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    await conversation.delete()
    return EndConversationResponse(status="Conversation ended")