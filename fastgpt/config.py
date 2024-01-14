import os

DEFAULT_LLM_API_NAME = "llama"

DOCKER_HOST = "tcp://docker.local:2375"
LLM_APIS = {
    "openai": {
        "url": "https://api.openai.com/v1",
        "model": "gpt-4",
        "key": os.environ["OPENAI_API_KEY"],
    },
    "llama": {
        "url": "http://localhost:8080/v1",
        "model": "deepseek-coder-33b",
        "key": "sk-2f2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b",
    },
}

SYSTEM_MESSAGE = {
    "python": {
        "role": "system",
        "content": "You are a smart and friendly AGI. You are especially an extremely good programmer.  Please follow the instructions and provide all code asked for in a code block.  Do not test, analyze, or run the code. ",
    }
}

MAX_TOKENS = 4096  # oops 1024 * 1024 * 128
