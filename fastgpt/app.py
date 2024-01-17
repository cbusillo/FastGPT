# app.py
from fastapi import Depends, FastAPI, WebSocket

# noinspection PyUnresolvedReferences
from modules.config import config
from modules.llm_communication import LLMClient
from modules.logger import setup_logger
from modules.middlewares import setup_middlewares
from modules.websocket_handler import WebSocketHandler, get_websocket_handler

app = FastAPI()
setup_middlewares(app)
logger = setup_logger()


@app.websocket("/generate")
async def websocket_generate(
    websocket: WebSocket,
    websocket_handler: WebSocketHandler = Depends(get_websocket_handler),
) -> None:
    await websocket_handler.websocket_generate(websocket)


@app.get("/models")
async def get_models() -> dict[str, list[str]]:
    logger.info("Sending models")
    return {"models": LLMClient.get_model_names()}
