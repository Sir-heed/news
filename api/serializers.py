from rest_framework import serializers
from story.models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ('editable',)

    