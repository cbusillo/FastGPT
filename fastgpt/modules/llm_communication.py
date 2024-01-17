# llm_communication.py
import subprocess
from glob import glob
from pathlib import Path
from typing import Generator
from urllib.parse import urlparse

import requests
from openai import AsyncOpenAI
from transformers import GPT2Tokenizer

from config import LLM_APIS, MAX_TOKENS, SYSTEM_MESSAGE
from .logging_config import setup_logging

logger = setup_logging(__name__)


class LLMClient:
    def __init__(self) -> None:
        self.models = {}
        for llm_model_name, llm_api in LLM_APIS.items():
            self.models[llm_model_name] = AsyncOpenAI(
                base_url=llm_api["url"],
                api_key=llm_api["key"],
            )
            if "8080" in llm_api["url"]:
                self.check_and_start_local_server(llm_model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    async def send_prompt(
        self, prompt_text: str, model_name: str, max_tokens: int = MAX_TOKENS
    ) -> Generator[str, None, None]:
        try:
            system_message = self._get_system_message()
            user_message = {"role": "user", "content": prompt_text}
            api_message = [system_message, user_message]

            num_tokens_used = sum(
                len(self.tokenizer.encode(message["content"], add_special_tokens=True))
                for message in [system_message, user_message]
            )

            adjusted_max_tokens = max_tokens - num_tokens_used

            response = await self.models[model_name].chat.completions.create(
                model=model_name,
                messages=api_message,
                max_tokens=adjusted_max_tokens,
                stream=True,
            )
            async for chunk in response:
                yield chunk.choices[0].delta.content
        except Exception as e:
            print(f"Error in sending prompt: {e}")

    @staticmethod
    def _get_system_message(language: str = "python") -> dict[str, str]:
        return SYSTEM_MESSAGE[language]

    @staticmethod
    def check_and_start_local_server(model_name: str) -> None:
        model_url = LLM_APIS[model_name]["url"]
        model_port = urlparse(model_url).port

        try:
            requests.get(f"{model_url}/health")
        except requests.exceptions.ConnectionError:
            script_path = Path(__file__).parent
            project_root = script_path.parent.absolute()
            server_binary = project_root / "external" / "llama.cpp" / "server"
            model_pattern = str(
                project_root / "models" / (model_name + "*" + "Q4" + "*.gguf")
            )

            if len(model_pattern) == 0:
                raise FileNotFoundError(f"Model file not found for {model_name}")
            model_file = glob(model_pattern)[0]
            command = [server_binary, "--port", model_port, "-m", model_file]
            logger.error(
                f"Starting local server using '{' '.join(str(text) for text in command)}'"
            )
            subprocess.Popen(command)

    @staticmethod
    def get_model_names() -> list[str]:
        for model_name in LLM_APIS.keys():
            yield model_name
