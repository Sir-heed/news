from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
ITEM_TYPE = (
        ("job", "job"),
        ("story", "story"),
        ("comment", "comment"),
        ("poll", "poll"),
        ("pollopt", "pollopt")
    )

class Item(models.Model):
    item_id = models.IntegerField(null=True)
    deleted = models.BooleanField(null=True)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE)
    by = models.CharField(max_length=100, null=True, blank=True)
    item_time = models.DateTimeField(null=True, blank=True)
    dead = models.BooleanField(null=True)
    kids = ArrayField(models.IntegerField(), null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    descendants = models.IntegerField(null=True)
    score = models.IntegerField(null=True)
    parent = models.IntegerField(null=True)
    parts = ArrayField(models.IntegerField(), null=True, blank=True)
    editable = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.item_id)