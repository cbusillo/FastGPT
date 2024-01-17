# app.py
import threading

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from asyncio import sleep

from websockets import ConnectionClosedOK

# noinspection PyUnresolvedReferences
from config import test_input
from modules.llm_communication import LLMClient
from modules.docker_interaction import DockerManager
from modules.code_validation import CodeValidator
from modules.logging_config import setup_logging
from modules.middlewares import setup_middlewares

app = FastAPI()
setup_middlewares(app)
logger = setup_logging(__name__)

llm_client = LLMClient()
docker_manager = DockerManager()

SLEEP_DURATION = 0.00001


@app.websocket("/generate")
async def websocket_generate(websocket: WebSocket) -> None:
    await websocket.accept()
    threading.Thread(target=docker_manager.start_container).start()
    await sleep(10)
    try:
        await process_websocket(websocket)
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except ConnectionClosedOK:
        logger.info("Connection closed")
    finally:
        threading.Thread(target=docker_manager.remove_container).start()


async def process_websocket(websocket: WebSocket) -> None:
    while True:
        data = await websocket.receive_json()
        prompt_text = data.get("prompt", "")
        model_name = data.get("model", "")
        await process_prompt(websocket, prompt_text, model_name=model_name)


async def process_prompt(
    websocket: WebSocket, prompt_text: str, model_name: str
) -> None:
    response_generator = llm_client.send_prompt(prompt_text, model_name)
    full_response = ""
    async for chunk in response_generator:
        if not chunk:
            continue
        full_response += chunk
        await websocket.send_json({"response": chunk})
        await sleep(SLEEP_DURATION)
    # full_response = Config.test_input
    await process_code_blocks(websocket, full_response)


async def process_code_blocks(websocket: WebSocket, full_response: str) -> None:
    code_blocks = CodeValidator.extract_code_blocks(full_response)
    if not code_blocks:
        return
    for language, code_block in code_blocks:
        await process_code_block(websocket, code_block)


async def process_code_block(websocket: WebSocket, code_block: str) -> None:
    if CodeValidator.is_valid_python(code_block):
        formatted_code = CodeValidator.format_with_black(code_block)
        code_imports = CodeValidator.extract_python_imports(formatted_code)
        code_imports = [
            import_name.replace("BeautifulSoup", "BeautifulSoup4")
            for import_name in code_imports
        ]
        pip_output = docker_manager.execute_pip_install(code_imports)
        await websocket.send_json({"code": pip_output})
        error_count, warning_count, messages = CodeValidator.run_pylint_static_analysis(
            formatted_code
        )
        if error_count > 0:
            logger.error(
                f"Code block has {error_count} errors, {warning_count} warnings: {messages}"
            )

        await execute_and_send_code(websocket, formatted_code)


async def execute_and_send_code(websocket: WebSocket, code: str) -> None:
    docker_output = docker_manager.execute_python(code)
    await websocket.send_json({"code": docker_output})
    await sleep(SLEEP_DURATION)


@app.get("/models")
async def get_models() -> dict[str, list[str]]:
    logger.info("Sending models")
    return {"models": llm_client.get_model_names()}
