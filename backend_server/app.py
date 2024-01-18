# app.py
from fastapi import FastAPI

from components.logger import setup_logger
from components.middlewares import setup_middlewares

from routes import generate, models

app = FastAPI()
setup_middlewares(app)
logger = setup_logger()

app.include_router(generate.router)
app.include_router(models.router)
