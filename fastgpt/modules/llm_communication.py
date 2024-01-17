# llm_communication.py
import logging
import subprocess
from glob import glob
from pathlib import Path
from typing import Generator
from urllib.parse import urlparse

import requests
import openai
from transformers import GPT2Tokenizer

from modules.config import config

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self) -> None:
        self.models = {}
        for llm_model_name, llm_api in config["LLM_APIS"].items():
            self.models[llm_model_name] = openai.AsyncOpenAI(
                base_url=llm_api["url"],
                api_key=llm_api["key"],
            )
            if "8080" in llm_api["url"]:
                self.check_and_start_local_server(llm_model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    async def send_prompt(
        self, prompt_text: str, model_name: str
    ) -> Generator[str, None, None]:
        llm_api = config["LLM_APIS"][model_name]
        system_message = self._get_system_message()
        user_message = {"role": "user", "content": prompt_text}
        api_message = [system_message, user_message]
        max_context_tokens = llm_api["max_context_tokens"]
        max_output_tokens = llm_api.get("max_output_tokens", None)
        if max_output_tokens:
            adjusted_max_tokens = max_output_tokens
        else:
            num_tokens_used = sum(
                len(
                    self.tokenizer.encode(
                        message["content"],
                        add_special_tokens=True,
                        max_length=max_context_tokens,
                        truncation=True,
                    )
                )
                for message in [system_message, user_message]
            )
            adjusted_max_tokens = max_context_tokens - num_tokens_used

        if adjusted_max_tokens <= config.get("MINIMUM_COMPLETION_TOKENS", 0):
            message = f"Adjusted max tokens ({adjusted_max_tokens}) is too low for model {model_name}"
            logger.warning(message)
            yield message
            return
        try:
            response = await self.models[model_name].chat.completions.create(
                model=model_name,
                messages=api_message,
                max_tokens=adjusted_max_tokens,
                stream=True,
            )
            async for chunk in response:
                yield chunk.choices[0].delta.content

        except openai.Timeout as e:
            logger.warning(f"OpenAI API request timed out: {e}")
        except openai.APIConnectionError as e:
            logger.warning(f"OpenAI API request failed to connect: {e}")
        except openai.BadRequestError as e:
            logger.warning(f"OpenAI API request was invalid: {e}")
        except openai.APIError as e:
            logger.warning(f"OpenAI API returned an API Error: {e}")
        except openai.AuthenticationError as e:
            logger.warning(f"OpenAI API request was not authorized: {e}")
        except openai.PermissionDeniedError as e:
            logger.warning(f"OpenAI API request was not permitted: {e}")
        except openai.RateLimitError as e:
            logger.warning(f"OpenAI API request exceeded rate limit: {e}")

    @staticmethod
    def _get_system_message(language: str = "python") -> dict[str, str]:
        return config["SYSTEM_MESSAGE"][language]

    @staticmethod
    def check_and_start_local_server(model_name: str) -> None:
        model_url = config["LLM_APIS"][model_name]["url"]
        model_port = urlparse(model_url).port
        model_port_str = str(model_port)

        try:
            requests.get(f"{model_url}/health")
        except requests.exceptions.ConnectionError:
            script_path = Path(__file__).parent
            project_root = script_path.parent.parent.absolute()
            server_binary = project_root / "external" / "llama.cpp" / "server"
            model_pattern = str(
                project_root / "models" / (model_name + "*" + "Q4" + "*.gguf")
            )

            if len(model_pattern) == 0:
                raise FileNotFoundError(f"Model file not found for {model_name}")
            model_file = glob(model_pattern)[0]
            command = [server_binary, "--port", model_port_str, "-m", model_file]
            command_str = " ".join(str(text) for text in command)
            logger.info(f"Starting local server using '{command_str}'")
            subprocess.Popen(command)

    @staticmethod
    def get_model_names() -> list[str]:
        for model_name in config["LLM_APIS"].keys():
            yield model_name
