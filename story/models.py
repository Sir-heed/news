from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.
STORY_TYPE = (
        ("job", "job"),
        ("story", "story"),
        ("comment", "comment"),
        ("poll", "poll"),
        ("pollopt", "pollopt")
    )

class Story(models.Model):
    story_id = models.IntegerField(unique=True)
    deleted = models.BooleanField(null=True, blank=True)
    story_type = models.CharField(max_length=10, choices=STORY_TYPE)
    by = models.CharField(max_length=100, null=True, blank=True)
    time = models.IntegerField(null=True, blank=True)
    dead = models.BooleanField(null=True, blank=True)
    kids = ArrayField(models.IntegerField(), null=True, blank=True)
    descendants = models.IntegerField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    editable = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.story_id


class Comment(models.Model):
    comment_id = models.IntegerField(unique=True)
    deleted = models.BooleanField(null=True, blank=True)
    comment_type = models.CharField(max_length=10, choices=STORY_TYPE)
    by = models.CharField(max_length=100, null=True, blank=True)
    time = models.IntegerField(null=True, blank=True)
    dead = models.BooleanField(null=True, blank=True)
    kids = ArrayField(models.IntegerField(), null=True, blank=True)
    parent = models.IntegerField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.comment_id)