from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import StoryViewSet, LatestNews, index, detail

router = DefaultRouter()
router.register('story', StoryViewSet, 'story')

urlpatterns = router.urls

urlpatterns += [
    path('home/', index, name='index'),
    path('home/<int:story_id>/', detail, name='detail'),
    path('latest/', LatestNews.as_view()),
]