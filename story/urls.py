from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from story.api import ItemViewSets
from .views import index, detail, create_item, edit_item, delete_item

app_name = 'story'

router = DefaultRouter()
router.register('items', ItemViewSets)

urlpatterns = [
    path('', index, name='index'),
    path('api/', include(router.urls)),
    path('detail/<int:pk>', detail, name='detail'),
    path('item-create', create_item, name='item-create'),
    path('item-edit/<int:pk>', edit_item, name='item-edit'),
    path('item-delete/<int:pk>', delete_item, name='item-delete'),
]