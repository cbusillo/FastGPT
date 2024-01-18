# routes/conversations.py
from fastapi import APIRouter, HTTPException
from backend_server.database.models.conversations import Conversation, Message

router = APIRouter()


@router.post("/conversations")
async def start_conversation(model_name: str) -> dict[str, str]:
    try:
        conversation = await Conversation.create(model_name=model_name)
        return {"conversation_id": str(conversation.id)}
    except Exception as e:
        raise HTTPException(
            status_code=400, detail={"error": str(e), "model_name": model_name}
        )


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str) -> dict[str, list[dict[str, str]]]:
    conversation = await Conversation.get_or_none(id=conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = await conversation.messages.all()
    return {"messages": [message.message for message in messages]}


@router.post("/conversations/{conversation_id}/messages")
async def add_message(
    conversation_id: str, message: str, sender: str
) -> dict[str, str]:
    conversation = await Conversation.get_or_none(id=conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    await Message.create(
        conversation_id=conversation_id, sender=sender, message=message
    )
    return {"status": "Message added"}


@router.delete("/conversations/{conversation_id}")
async def end_conversation(conversation_id: str) -> dict[str, str]:
    conversation = await Conversation.get_or_none(id=conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    await conversation.delete()
    return {"status": "Conversation ended"}
