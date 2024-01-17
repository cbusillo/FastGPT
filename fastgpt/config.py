import os

MINIMUM_COMPLETION_TOKENS = 100

_DOCKER_HOST = "docker.local"
_DOCKER_PORT = 2375

DOCKER_URL = f"tcp://{_DOCKER_HOST}:{_DOCKER_PORT}"

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

SYSTEM_MESSAGE = {
    "python": {
        "role": "system",
        "content": """
You are an extremely good programmer. Provide all code in code blocks with no comments.  
All code in the same file should be in the same codeblock. Put the langauge you 
are using in the first line of the code block. 
If the module name does not match a pypi package please use bash and pip to install it. 
To run commands in the shell, use bash at the top of the codeblock.  Put the bash codeblock first.  
This is executing in a docker container.  Do not user interactive commands like input. 
Docker is very limited in commands, but you can use apt to install packages.  
We are targeting pythin 3.11, FastAPI 0.109.0, and React.js 18.2.0.  Provide the best code you can.
Focus on being clean and pythonic.
""",
    }
}


# noinspection LongLine,HttpUrlsUsage,SpellCheckingInspection
TEST_INPUT = """
```bash
pip install ping3
```

Then, you can create a Python script with the following code:

```python
from ping3 import ping

def ping_host(host):
    try:
        response_time = ping(host)
        if response_time is None:
            print(f"{host} is not reachable.")
        else:
            print(f"{host} is reachable in {response_time}s.")
    except exceptions.PingError as e:
        print(f"An error occurred while pinging {host}: {e}")

if __name__ == "__main__":
    host = input("Enter a host to ping: ")
    ping_host(host)
```

This script will prompt the user for a host to ping and then print out whether the host is reachable and how long it took to respond. If an error occurs, it will print that as well.
"""
