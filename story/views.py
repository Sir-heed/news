import requests
from requests.exceptions import ConnectionError
from django.db.utils import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from .models import Story, Comment
from .serializers import StorySerializer

# Create your views here.
top_stories_url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
news = 'https://hacker-news.firebaseio.com/v0/item/{}.json'


def index(request):
    latest_news = Story.objects.order_by('id')[:20]
    output = ', '.join([q.url for q in latest_news])
    return HttpResponse(output)

class StoryViewSet(ModelViewSet):
    queryset = Story.objects.filter(editable=True)
    serializer_class = StorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['story_type']

    def list(self, request):
        queryset = Story.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        story = Story.objects.get(pk=pk)
        return Response(StorySerializer(story).data, status=status.HTTP_200_OK)


class LatestNews(APIView):
    def get(self, request):
        try:
            r = requests.get(top_stories_url)
            if r.status_code == 200:
                top_stories = r.json()
                for item in top_stories[:20]:
                    r = requests.get(news.format(item))
                    if r.status_code == 200:
                        res = r.json()
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
                        except IntegrityError:
                            print("Story saved already")
                            pass
                else:
                    return Response({
                    'status':'success',
                    'message':'Data saved to database'
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'status':'failed',
                    'message':'Unable to connect to hacker news'
                }, status=status.HTTP_408_REQUEST_TIMEOUT)
        except ConnectionError:
            return Response({
                'status': 'failed',
                'message': 'Unable to connect to hacker news'
            }, status=status.HTTP_408_REQUEST_TIMEOUT)