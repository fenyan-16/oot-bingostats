from django.db import models
from django.contrib.auth.models import User
import numpy as np
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField
from tournament.models import Tournament


# Create your models here.
class League(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, null=True)
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.name)


class TournamentsInLeague(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.league) + str(self.tournament)


class Ratingpoints(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(null=True)

    def __str__(self):
        return str(self.league) + str(self.tournament)