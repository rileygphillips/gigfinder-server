from django.db import models


class Instrument(models.Model):
    label = models.CharField(max_length=50)