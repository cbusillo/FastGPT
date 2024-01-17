# app.py
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from asyncio import sleep

from websockets import ConnectionClosedOK

# noinspection PyUnresolvedReferences
from config import TEST_INPUT
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
    executor = ThreadPoolExecutor()
    executor.submit(docker_manager.start_container)
    try:
        await process_websocket(websocket)
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except ConnectionClosedOK:
        logger.info("Connection closed")
    finally:
        executor.submit(docker_manager.remove_container)


async def process_websocket(websocket: WebSocket) -> None:
    while True:
        data = await websocket.receive_json()
        prompt_text = data.get("prompt", "")
        model_name = data.get("model", "")
        test_input = data.get("test_input", "")
        await process_prompt(
            websocket, prompt_text, model_name=model_name, test_input=test_input
        )


async def process_prompt(
    websocket: WebSocket, prompt_text: str, model_name: str, test_input: bool
) -> None:
    if test_input:
        full_response = TEST_INPUT
        await websocket.send_json({"response": full_response})
        await sleep(SLEEP_DURATION)
    else:
        response_generator = llm_client.send_prompt(prompt_text, model_name)
        full_response = ""
        async for chunk in response_generator:
            if not chunk:
                continue
            full_response += chunk
            await websocket.send_json({"response": chunk})
            await sleep(SLEEP_DURATION)

    await process_code_blocks(websocket, full_response)


async def process_code_blocks(websocket: WebSocket, full_response: str) -> None:
    code_blocks_with_language = CodeValidator.extract_code_blocks(full_response)
    if not code_blocks_with_language:
        return
    for language, code_block in code_blocks_with_language:
        await process_code_block(websocket, code_block, language)


async def process_code_block(websocket: WebSocket, code_block: str, language) -> None:
    if language in ["bash", "sh", "shell"]:
        _exit_code, bash_output = docker_manager.execute_bash(code_block)
        code_output = code_block + "\n\n" + bash_output + "=" * 50
        await websocket.send_json({"code": code_output})
        await sleep(SLEEP_DURATION)
    if language in ["py", "python"] and CodeValidator.is_valid_python(code_block):
        formatted_code = CodeValidator.format_with_black(code_block)
        code_imports = CodeValidator.extract_python_imports(formatted_code)
        pip_output = docker_manager.execute_pip_install(code_imports)
        await sleep(SLEEP_DURATION)
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
    docker_output = docker_manager.execute_python_string(code)
    await websocket.send_json({"code": docker_output})
    await sleep(SLEEP_DURATION)


@app.get("/models")
async def get_models() -> dict[str, list[str]]:
    logger.info("Sending models")
    return {"models": llm_client.get_model_names()}
