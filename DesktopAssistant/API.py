
import os
import datetime
from newsapi import NewsApiClient
import re
from dotenv import load_dotenv
import requests
from wolframalpha import Client

load_dotenv(dotenv_path='Data\\.env')
NEWS = os.getenv('NEWS_API')
news = NewsApiClient(api_key=NEWS)

def get_ip(_return=False):
    try:
        response = requests.get(f'http://ip-api.com/json/').json()
        if _return:
            return response
        else:
            return f'Your IP address is {response["query"]}'
    except KeyboardInterrupt:
        return None
    except requests.exceptions.RequestException:
        return None

def get_news():
    try:
        top_news = ""
        top_headlines = news.get_top_headlines(language="en", country="in")
        for i in range(10):
             top_news += re.sub(r'[|-] [A-Za-z0-9 |:.]*', '', top_headlines['articles'][i]['title']).replace("’", "'") + '\n'
        return top_news
    except KeyboardInterrupt:
        return None
    except requests.exceptions.RequestException:
        return None
def get_joke():
    try:
        joke = requests.get('https://v2.jokeapi.dev/joke/Any?format=txt').text
        return joke
    except KeyboardInterrupt:
        return None
    except requests.exceptions.RequestException:
        return None