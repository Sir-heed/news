from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ItemViewSet

router = DefaultRouter(trailing_slash=False)

router.register('', ItemViewSet)

urlpatterns = router.urls

urlpatterns += [
]

