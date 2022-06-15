from django.db import models
from django.contrib.auth.models import User


class Musician(models.Model):
    musician = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    bio = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    skill_level = models.ForeignKey("SkillLevel", on_delete=models.CASCADE)
    resume_link = models.CharField(max_length=200)
    audition_video_link = models.CharField(max_length=200)
    instruments = models.ForeignKey("Instrument", on_delete=models.CASCADE)
    photo_link =  models.CharField(max_length=200)