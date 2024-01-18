# app.py
from fastapi import FastAPI

from components.logger import setup_logger
from components.middlewares import setup_middlewares
from database.sqlite import database

from routes import generate, models, conversations

app = FastAPI()
setup_middlewares(app)
logger = setup_logger()

app.include_router(generate.router)
app.include_router(models.router)
app.include_router(conversations.router)


@app.on_event("startup")
async def startup() -> None:
    await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()
