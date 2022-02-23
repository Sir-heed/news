# Create your tasks here
import requests
from celery import shared_task
from datetime import datetime
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from django.db.utils import IntegrityError
from.utils import get_max_news_id
from .models import Item

top_stories_url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
news = 'https://hacker-news.firebaseio.com/v0/item/{}.json'

logger = get_task_logger(__name__)


@shared_task
def sample_task():
    logger.info("The sample task just ran.")
    

@shared_task
def get_latest_news():
    max_ind = get_max_news_id()
    if max_ind is not None:
        max_ind = int(max_ind)
        for item in range(max_ind - 100, max_ind):
            r = requests.get(news.format(item))
            if r.status_code == 200:
                data = r.json()
                print(data)
                try:
                    item = Item.objects.get(item_id=data.get('id'))
                except Item.DoesNotExist:
                    Item.objects.create(
                        item_id = data.get('id'),
                        deleted = data.get('deleted'),
                        item_type = data.get('type'),
                        by = data.get('by'),
                        item_time = datetime.fromtimestamp(data.get('time')) if data.get('time') else None,
                        dead = data.get('dead'),
                        kids = data.get('kids'),
                        text = data.get('text'),
                        url = data.get('url'),
                        title = data.get('title'),
                        descendants = data.get('descendants'),
                        score = data.get('score'),
                        parent = data.get('parent'),
                        parts = data.get('parts'),
                        editable = False
                    )
            else:
                print('Not Available')
    else:
        return None