from django.db import models
from django.contrib.auth.models import User


class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    bio = models.CharField(max_length=200)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)
    music_link = models.CharField(max_length=200)
    website_link = models.CharField(max_length=200)
    photo_link = models.CharField(max_length=200)
    