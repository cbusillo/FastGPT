# app.py
import logging

from fastapi import FastAPI

from components.logger import setup_logger
from components.middlewares import setup_middlewares

from routes import generate, models, conversations
from database import orm_interface

app = FastAPI()
setup_middlewares(app)
logger = setup_logger()
logging.basicConfig(level=logging.DEBUG)

app.include_router(generate.router)
app.include_router(models.router)
app.include_router(conversations.router)


@app.on_event("startup")
async def startup_event() -> None:
    await orm_interface.start()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await orm_interface.stop()
