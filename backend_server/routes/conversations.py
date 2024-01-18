# routes/conversations.py
from fastapi import APIRouter, HTTPException
from sqlalchemy import select, delete
from database.sqlite import database, engine, metadata
from database.models.conversations import conversations, messages

router = APIRouter()

# Create the database
metadata.create_all(engine)


@router.post("/conversations")
async def start_conversation(model_name: str) -> dict[str, str]:
    query = conversations.insert().values(model_name=model_name)
    last_record_id = await database.execute(query)
    return {"conversation_id": str(last_record_id)}


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str) -> dict[str, list[dict[str, str]]]:
    query = select([conversations]).where(conversations.c.id == conversation_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"messages": result}


@router.post("/conversations/{conversation_id}/messages")
async def add_message(
    conversation_id: str, message: str, sender: str
) -> dict[str, str]:
    query = messages.insert().values(
        conversation_id=conversation_id, sender=sender, message=message
    )
    await database.execute(query)
    return {"status": "Message added"}


@router.delete("/conversations/{conversation_id}")
async def end_conversation(conversation_id: str) -> dict[str, str]:
    query = delete(conversations).where(conversations.c.id == conversation_id)
    await database.execute(query)
    return {"status": "Conversation ended"}
