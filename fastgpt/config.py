import os

DOCKER_HOST = "tcp://docker.local:2375"
# noinspection SpellCheckingInspection
LLM_APIS = {
    "llama.cpp": {
        "url": "http://localhost:8080/v1",
        "model": "phind-codellama-34",
        "key": "sk-2f2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b",
    },
    "openai": {
        "url": "https://api.openai.com/v1",
        "model": "gpt-4",
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

# noinspection LongLine
test_prompt = """
Write a Python script that generates a list of random integers between 1 and 100. The script should then calculate and print the mean, median, and standard deviation of these numbers. Use the 'random' module to generate the list and 'statistics' module for the calculations. Ensure to include necessary imports and handle any potential errors.
"""

# noinspection LongLine,HttpUrlsUsage
test_input = """
This task could be accomplished using Python with Requests and Beautiful Soup (for web scraping) alongside the OpenWeather helper modules. Although public APIs to get the largest cities are not readily available, we can use Beautiful Soup to scrape from a wikipedia page holding this list. For weather, we will use the OpenWeatherMap API.

The code below first scrapes the 5 largest cities from wikipedia, then uses its names to gather weather data from OpenWeatherMap API.

NOTE: You would have to sign up on openweathermap.org and get your own API key, as it is specific to each user and then replace `YOUR_OPEN_WEATHER_API_KEY` with your own OpenWeatherMap API key.

Also, as the task explicitly mentions not to test, analyze or run the code, it's provided as is. However, BeautifulSoup implements methods to select specific elements in webpage, which may include select(), select_one(), find(), find_all() etc, so the method used below to select city names may change based on the structure of the webpage.


```
python
import requests
from bs4 import BeautifulSoup
import json

# URL for the wiki page about the world's largest cities
url = 'https://en.wikipedia.org/wiki/List_of_largest_cities'

# send a GET request to the URL
response = requests.get(url)

# parse the content with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# find the table in the HTML that contains the cities
table = soup.find('table', {'class': 'wikitable sortable'})

# find all the rows within the table
rows = table.find_all('tr')

# list to store cities
cities = []

# iterate over the rows
for row in rows[1:6]:  # get first 5 rows excluding headings
    city_name = row.find('a').text  # get city name
    cities.append(city_name)

# OpenWeatherMap API url
api_url = 'http://api.openweathermap.org/data/2.5/weather'

# iterate over cities to get their weather info
for city in cities:
    parameters = {
        'q': city,
        'appid': 'YOUR_OPEN_WEATHER_API_KEY'
    }
    city_response = requests.get(api_url, params=parameters)

    if city_response.status_code == 200:  # status code 200 indicates success
        # parse the response from JSON into a Python dictionary
        city_weather = json.loads(city_response.text)
        print(f"Weather in {city}: {city_weather['weather'][0]['description']}")
    else:
        print(f"Couldn't get weather information for {city}. Check city name or Open Weather API key.")
```
Please consider that web scraping Wikipedia or any other site must comply with their terms of service. For robustness and reliability, a dedicated API or dataset is recommended for such tasks. The OpenWeatherMap API is also subjected to limitations in free plan (e.g., a limited number of requests per minute).

"""
