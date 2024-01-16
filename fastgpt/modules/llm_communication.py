import subprocess
from glob import glob
from pathlib import Path
from typing import Generator

import openai
import requests
from transformers import GPT2Tokenizer

from config import LLM_APIS, MAX_TOKENS, SYSTEM_MESSAGE
from .logging_config import setup_logging

logger = setup_logging(__name__)


class LLMClient:
    def __init__(self, llm_api_name: str = list(LLM_APIS.keys())[0]) -> None:
        self.llm_api = LLM_APIS[llm_api_name]
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

        if llm_api_name == "llama.cpp":
            self.check_and_start_local_server()

        self.client = openai.AsyncOpenAI(
            base_url=self.llm_api["url"], api_key=self.llm_api["key"]
        )

    async def send_prompt(
        self, prompt_text: str, max_tokens: int = MAX_TOKENS
    ) -> Generator[str, None, None]:
        try:
            system_message = self._get_system_message()
            user_message = {"role": "user", "content": prompt_text}

            num_tokens_used = sum(
                len(self.tokenizer.encode(message["content"], add_special_tokens=True))
                for message in [system_message, user_message]
            )

            adjusted_max_tokens = max_tokens - num_tokens_used

            response = await self.client.chat.completions.create(
                model=self.llm_api["model"],
                messages=[system_message, user_message],
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

    def check_and_start_local_server(self) -> None:
        url = self.llm_api["url"]
        try:
            requests.get(f"{url}/health")
        except requests.exceptions.ConnectionError:
            script_path = Path(__file__).parent
            project_root = script_path.parent.absolute()
            server_binary = project_root / "external" / "llama.cpp" / "server"
            model_pattern = str(
                project_root
                / "models"
                / (self.llm_api["model"] + "*" + "Q4" + "*.gguf")
            )

            if len(model_pattern) == 0:
                raise FileNotFoundError(
                    f"Model file not found for {self.llm_api['model']}"
                )
            model_file = glob(model_pattern)[0]
            command = [server_binary, "-m", model_file]
            logger.error(
                f"Starting local server using '{' '.join(str(text) for text in command)}'"
            )
            subprocess.Popen(command)

    @staticmethod
    def get_model_names() -> list[str]:
        for model_name in LLM_APIS.keys():
            yield model_name
