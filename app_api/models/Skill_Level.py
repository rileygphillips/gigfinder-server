from django.db import models


class SkillLevel(models.Model):
    label = models.CharField(max_length=50)