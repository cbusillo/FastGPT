# conversations.py
from tortoise.models import Model
from tortoise import fields


class Conversation(Model):
    id = fields.UUIDField(pk=True)
    model_name = fields.CharField(max_length=255, index=True)


class Message(Model):
    id = fields.UUIDField(pk=True)
    conversation_id = fields.ForeignKeyField(
        "models.Conversation", related_name="messages"
    )
    sender = fields.CharField(max_length=255, index=True)
    message = fields.TextField()
