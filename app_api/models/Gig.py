from django.db import models


class Gig(models.Model):
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE)
    gig_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    date = models.DateTimeField()
    description = models.CharField(max_length=300)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)
    venue = models.CharField(max_length=100)
    skill_level_needed = models.ForeignKey("SkillLevel", on_delete=models.CASCADE)
    instruments_needed = models.ForeignKey("Instrument", on_delete=models.CASCADE)
    photo_link = models.CharField(max_length=200)
    gigs_submitted_to = models.ManyToManyField("Musician", related_name="gigs")