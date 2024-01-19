import os
from pathlib import Path

from dotenv import load_dotenv
from tomlkit import parse

load_dotenv()

class Config:
    def __init__(self) -> None:
        self._toml_config = None
        self.SYSTEM_MESSAGES_FILE = (
            Path(__file__).parent.parent / "data" / "system_messages.toml"
        )
        self.SYSTEM_MESSAGES = {}
        self.TEST_INPUT = None
        self._load_system_messages()

    def _load_system_messages(self) -> None:
        with open(self.SYSTEM_MESSAGES_FILE) as file:
            self._toml_config = parse(file.read())
        languages = ["python"]
        for language in languages:
            system_message = self._toml_config["SYSTEM_MESSAGE"].get(language, None)
            self.SYSTEM_MESSAGES[language] = {
                "role": "system",
                "content": system_message,
            }

        self.TEST_INPUT = self._toml_config["TEST_MESSAGES"].get("input", None)

    def reload(self) -> None:
        self._load_system_messages()

    MINIMUM_COMPLETION_TOKENS = 100

    _DOCKER_HOST = "docker.local"
    _DOCKER_PORT = 2375

    DOCKER_URL = f"tcp://{_DOCKER_HOST}:{_DOCKER_PORT}"

    SLEEP_DURATION = 0.00001

    RECOGNIZED_LANGUAGES = ["python", "js", "javascript"]

    PYLINT_DISABLED_CHECKS = ["C0114", "C0116"]

    # noinspection SpellCheckingInspection
    LLM_APIS = {
        "phind-codellama-34": {
            "url": "http://localhost:8080/v1",
            "key": "sk-2f2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b",
            "max_context_tokens": 4 * 1024,
        },
        "gpt-4": {
            "url": "https://api.openai.com/v1",
            "key": os.environ["OPENAI_API_KEY"],
            "max_context_tokens": 8 * 1024,
        },
        "gpt-4-1106-preview": {
            "url": "https://api.openai.com/v1",
            "key": os.environ["OPENAI_API_KEY"],
            "max_context_tokens": 120_000,
            "max_output_tokens": 4 * 1024,
        },
        "gpt-3.5-turbo-16k": {
            "url": "https://api.openai.com/v1",
            "key": os.environ["OPENAI_API_KEY"],
            "max_context_tokens": 16 * 1024,
        },
        "gpt-3.5-turbo-1106": {
            "url": "https://api.openai.com/v1",
            "key": os.environ["OPENAI_API_KEY"],
            "max_context_tokens": 16 * 1024,
            "max_output_tokens": 4 * 1024,
        },
    }


config = Config()
