import requests
from datetime import datetime
from .models import Item

base_url = 'https://hacker-news.firebaseio.com/v0'
news = 'https://hacker-news.firebaseio.com/v0/item/{}.json'

def get_max_news_id():
    r = requests.get(f'{base_url}/maxitem.json')
    if r.status_code == 200:
        return r.json()
    else:
        return None