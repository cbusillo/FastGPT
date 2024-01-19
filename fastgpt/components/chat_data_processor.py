# data_processor.py
from asyncio import sleep

from fastapi import WebSocket

from components.code_validation import CodeValidator
from components.config import config
from components.docker_interface import DockerManager
from components.lang_model_service import LLMClient
from components.logger import setup_logger

logger = setup_logger()


class ChatDataProcessor:
    def __init__(
        self, docker_manager: DockerManager, websocket: WebSocket, llm_client: LLMClient
    ) -> None:
        self.docker_manager = docker_manager
        self.websocket = websocket
        self.llm_client = llm_client

    async def process_prompt(
        self, prompt_text: str, model_name: str, test_input: bool
    ) -> None:
        if test_input:
            full_response = config.TEST_INPUT
            await self.websocket.send_json({"response": full_response})
            await sleep(config.SLEEP_DURATION)
        else:
            response_generator = self.llm_client.send_prompt(prompt_text, model_name)
            full_response = ""
            async for chunk in response_generator:
                if not chunk:
                    continue
                full_response += chunk
                await self.websocket.send_json({"response": chunk})
                await sleep(config.SLEEP_DURATION)

        await self.process_code_blocks(full_response)

    async def process_code_blocks(self, full_response: str) -> None:
        code_blocks_with_language = CodeValidator.extract_code_blocks(full_response)
        if not code_blocks_with_language:
            return
        for language, code_block in code_blocks_with_language:
            await self.process_code_block(code_block, language)

    async def process_code_block(self, code_block: str, language) -> None:
        if language in ["bash", "sh", "shell"]:
            _exit_code, bash_output = self.docker_manager.execute_bash(code_block)
            code_output = code_block + "\n\n" + bash_output + "=" * 50
            await self.websocket.send_json({"code": code_output})
            await sleep(config.SLEEP_DURATION)

        if language in ["py", "python"] and CodeValidator.is_valid_python(code_block):
            formatted_code = CodeValidator.format_with_black(code_block)
            code_imports = CodeValidator.extract_python_imports(formatted_code)
            pip_output = self.docker_manager.execute_pip_install(code_imports)
            await sleep(config.SLEEP_DURATION)
            await self.websocket.send_json({"code": pip_output})
            (
                error_count,
                warning_count,
                messages,
            ) = CodeValidator.run_pylint_static_analysis(formatted_code)
            if error_count > 0:
                logger.error(
                    f"Code block has {error_count} errors, {warning_count} warnings: {messages}"
                )

            await self.execute_and_send_code(formatted_code)

    async def execute_and_send_code(self, code: str) -> None:
        docker_output = self.docker_manager.execute_python_string(code)
        await self.websocket.send_json({"code": docker_output})
        await sleep(config.SLEEP_DURATION)
