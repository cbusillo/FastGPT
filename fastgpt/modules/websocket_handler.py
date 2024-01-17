# websocket_handler.py
import logging
from concurrent.futures import ThreadPoolExecutor
from fastapi import WebSocket, WebSocketDisconnect
from websockets import ConnectionClosedOK

from modules.config import config
from modules.data_processor import DataProcessor
from modules.docker_interaction import DockerManager
from modules.llm_communication import LLMClient

logger = logging.getLogger(__name__)


class WebSocketHandler:
    def __init__(self) -> None:
        self.docker_manager = DockerManager()
        self.llm_client = LLMClient()
        self.websocket = None
        self.data_processor = None

    async def websocket_generate(self, websocket: WebSocket) -> None:
        self.websocket = websocket
        self.data_processor = DataProcessor(
            self.docker_manager, self.websocket, self.llm_client
        )
        await self.websocket.accept()
        config.reload()
        executor = ThreadPoolExecutor()
        executor.submit(self.docker_manager.start_container)
        try:
            await self.process_websocket()
        except WebSocketDisconnect:
            logger.info("Client disconnected")
        except ConnectionClosedOK:
            logger.info("Connection closed")
        finally:
            executor.submit(self.docker_manager.remove_container)

    async def process_websocket(self) -> None:
        while True:
            data = await self.websocket.receive_json()
            prompt_text = data.get("prompt", "")
            model_name = data.get("model", "")
            test_input = data.get("test_input", "")
            await self.data_processor.process_prompt(
                prompt_text, model_name=model_name, test_input=test_input
            )


def get_websocket_handler() -> WebSocketHandler:
    return WebSocketHandler()
