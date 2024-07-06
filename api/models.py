from django.db import models
from django.contrib.postgres.fields import ArrayField

class User(models.Model):
    spotify_id = models.CharField(max_length=100, unique=True)
    artists = ArrayField(models.CharField(blank=True),null=True, 
        blank=True, 
        default=list) 
