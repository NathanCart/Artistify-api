from django.db import models
from django.contrib.postgres.fields import ArrayField

class User(models.Model):
    spotify_id = models.CharField(max_length=100, unique=True)
    artists = ArrayField(models.CharField(blank=True, max_length=255),null=True,
        blank=True, 
        default=list, 
        max_length=255)
    friends = ArrayField(models.IntegerField(blank=True),null=True,
        blank=True,
        default=list,
        max_length=255)
    display_name = models.CharField(max_length=100, blank=True)
    avatar_url = models.TextField(blank=True, null=True)
    followers = models.IntegerField(blank=True, null=True)

