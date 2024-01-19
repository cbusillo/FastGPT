from fastapi import APIRouter, Depends, WebSocket
from components.websocket_handler import WebSocketHandler, get_websocket_handler

router = APIRouter()


@router.websocket("/generate")
async def websocket_generate(
    websocket: WebSocket,
    websocket_handler: WebSocketHandler = Depends(get_websocket_handler),
) -> None:
    await websocket_handler.websocket_generate(websocket)
