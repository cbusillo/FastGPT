from fastapi import APIRouter, HTTPException
from components.conversations import Conversation

router = APIRouter()

conversations = (
    {}
)  # This is a placeholder. You might want to replace this with a proper database or data store.


@router.post("/conversations")
async def start_conversation(model_name: str) -> dict[str, str]:
    conversation = Conversation(model_name)
    conversation_id = str(
        id(conversation)
    )  # This is a placeholder. You might want to replace this with a proper ID generation method.
    conversations[conversation_id] = conversation
    return {"conversation_id": conversation_id}


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str) -> dict[str, list[dict[str, str]]]:
    conversation = conversations.get(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"messages": conversation.get_messages()}


@router.post("/conversations/{conversation_id}/messages")
async def add_message(
    conversation_id: str, message: str, sender: str
) -> dict[str, str]:
    conversation = conversations.get(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    conversation.add_message(message, sender)
    return {"status": "Message added"}


@router.delete("/conversations/{conversation_id}")
async def end_conversation(conversation_id: str) -> dict[str, str]:
    conversation = conversations.get(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    del conversations[conversation_id]
    return {"status": "Conversation ended"}
