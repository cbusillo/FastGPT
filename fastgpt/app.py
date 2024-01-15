import logging

from fastapi import FastAPI, WebSocket
from starlette.middleware.cors import CORSMiddleware
from asyncio import sleep

from llm_communication import LLMClient
from docker_interaction import DockerManager
from code_validation import CodeValidator

app = FastAPI()
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_client = LLMClient()
docker_manager = DockerManager()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@app.websocket("/generate")
async def websocket_generate(websocket: WebSocket) -> None:
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        prompt_text = data.get("prompt", "")

        response_generator = llm_client.send_prompt(prompt_text)
        full_response = ""
        for chunk in response_generator:
            if not chunk:
                continue
            full_response += chunk
            await websocket.send_json({"response": chunk})
            await sleep(0.0000001)

        code_blocks = CodeValidator.extract_code_blocks(full_response)
        for code in code_blocks:
            if CodeValidator.is_valid_python(code):
                error_count, _, _ = CodeValidator.run_static_analysis(code)
                if error_count > 0:
                    continue
                formatted_code = CodeValidator.format_code(code)
                docker_output = docker_manager.run_code_in_container(formatted_code)
                await websocket.send_json({"code": docker_output})

        await websocket.send_json({"completed": True})
