import os


_DOCKER_HOST = "docker.local"
_DOCKER_PORT = 2375
_REDIS_HOST = _DOCKER_HOST
_REDIS_PORT = 6379

DOCKER_URL = f"tcp://{_DOCKER_HOST}:{_DOCKER_PORT}"
REDIS_URL = f"redis://{_REDIS_HOST}:{_REDIS_PORT}/0"
# noinspection SpellCheckingInspection
LLM_APIS = {
    "phind-codellama-34": {
        "url": "http://localhost:8080/v1",
        "key": "sk-2f2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b",
    },
    "gpt-4": {
        "url": "https://api.openai.com/v1",
        "key": os.environ["OPENAI_API_KEY"],
    },
    "gpt-4-1106-preview": {
        "url": "https://api.openai.com/v1",
        "key": os.environ["OPENAI_API_KEY"],
    },
}

SYSTEM_MESSAGE = {
    "python": {
        "role": "system",
        "content": "You are a smart and friendly AGI. You are especially an extremely good programmer.  \
        Please follow the instructions and provide all code asked for in a code block.  Do not test, \
        analyze, or run the code. Please put the langauge you are using in the first line of the code block. \
        Any code in codeblocks will execute in a docker environment.  Any imports will install matching deps. \
        from pypi automatically in docker.",
    }
}

MAX_TOKENS = 4096  # oops 1024 * 1024 * 128

# noinspection LongLine,HttpUrlsUsage,SpellCheckingInspection
TEST_INPUT = """
```python
import random
import statistics
import requests

try:
    # Generate a list of 100 random integers between 1 and 100000
    numbers = [random.randint(1, 100000) for _ in range(100)]
    
    print("Generated numbers:")
    print(numbers)

    # Calculate mean of the numbers
    mean_num = statistics.mean(numbers)
    print("Mean:", mean_num)

    # Calculate median of the numbers
    median_num = statistics.median(numbers)
    print("Median:", median_num)

    # Calculate standard deviation of the numbers
    std_dev_num = statistics.stdev(numbers)
    print("Standard Deviation:", std_dev_num)

except Exception as e:
    print("An error occurred:", str(e))
```
"""
