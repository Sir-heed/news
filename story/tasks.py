# Create your tasks here
import requests
from celery import shared_task
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from django.db.utils import IntegrityError
from .models import Story, Comment

top_stories_url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
news = 'https://hacker-news.firebaseio.com/v0/item/{}.json'

logger = get_task_logger(__name__)


@shared_task
def sample_task():
    logger.info("The sample task just ran.")

@shared_task
def update_stories():
    r = requests.get(top_stories_url)
    if r.status_code == 200:
        top_stories = r.json()
        for item in top_stories[:20]:
            r = requests.get(news.format(item))
            if r.status_code == 200:
                res = r.json()
                print("Story>>>>>>>>>>>>>>", res)
                try:
                    Story.objects.create(
                        by=res['by'] if 'by' in res else None,
                        descendants=res['descendants'] if 'descendants' in res else None,
                        story_id=res['id'],
                        kids=res['kids'] if 'kids' in res else None,
                        score=res['score'] if 'score' in res else None,
                        time=res['time'] if 'time' in res else None,
                        title=res['title'] if 'title' in res else None,
                        story_type=res['type'],
                        url=res['url'] if 'url' in res else None,
                        dead=res['dead'] if 'dead' in res else None,
                        deleted=res['deleted'] if 'deleted' in res else None,
                        editable=False
                    )
                    if 'kids' in res:
                        for item in res['kids']:
                            r = requests.get(news.format(item))
                            if r.status_code == 200:
                                res = r.json()
                                print("Comment>>>>>>>>>>>>>>", res)
                                try:
                                    Comment.objects.create(
                                        by = res['by'] if 'by' in res else None,
                                        comment_id = res['id'],
                                        parent = res['parent'] if 'parent' in res else None,
                                        text = res['text'] if 'text' in res else None,
                                        time = res['time'] if 'time' in res else None,
                                        comment_type=res['type'] if 'type' in res else None
                                    )
                                except IntegrityError:
                                    print("Comment saved already")
                                    pass
                except IntegrityError:
                    print("Story saved already")
                    pass


# def update_stories():
#     r = requests.get(top_stories_url)
#     if r.status_code == 200:
#         top_stories = r.json()
#         for item in top_stories[:20]:
#             r = requests.get(news.format(item))
#             if r.status_code == 200:
#                 res = r.json()
#                 try:
#                     Story.objects.create(
#                         by=res['by'] if 'by' in res else None,
#                         descendants=res['descendants'] if 'descendants' in res else None,
#                         story_id=res['id'],
#                         kids=res['kids'] if 'kids' in res else None,
#                         score=res['score'] if 'score' in res else None,
#                         time=res['time'] if 'time' in res else None,
#                         title=res['title'] if 'title' in res else None,
#                         story_type=res['type'],
#                         url=res['url'] if 'url' in res else None,
#                         dead=res['dead'] if 'dead' in res else None,
#                         deleted=res['deleted'] if 'deleted' in res else None,
#                         editable=False
#                     )
#                     print("Data stored")
#                 except IntegrityError:
#                     print("Story saved already")
#                     pass