from typing import Generator

import openai
from transformers import GPT2Tokenizer

from .config import LLM_APIS, SYSTEM_MESSAGE, MAX_TOKENS, DEFAULT_LLM_API_NAME


class LLMClient:
    def __init__(self, llm_api_name: str = DEFAULT_LLM_API_NAME) -> None:
        self.llm_api = LLM_APIS[llm_api_name]
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.client = openai.OpenAI(
            base_url=self.llm_api["url"], api_key=self.llm_api["key"]
        )

    def send_prompt(
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

            response = self.client.chat.completions.create(
                model=self.llm_api["model"],
                messages=[system_message, user_message],
                max_tokens=adjusted_max_tokens,
                stream=True,
            )
            for chunk in response:
                yield chunk.choices[0].delta.content
        except Exception as e:
            print(f"Error in sending prompt: {e}")
            return None

    @staticmethod
    def _get_system_message(language: str = "python") -> dict[str, str]:
        return SYSTEM_MESSAGE[language]
