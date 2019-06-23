from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class Event(models.Model):
    name = models.CharField(max_length=200)
    description_short = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=500, null=True)
    start_date = models.DateTimeField('Start date', null=True)
    end_date = models.DateTimeField('End date', null=True)
    location = models.CharField(max_length=200, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Tournament(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, null=True)
    name = models.CharField(max_length=200)
    max_participants = models.DecimalField(max_digits=5, decimal_places=0, null=True)

    def __str__(self):
        return self.name

class Phase(models.Model):
    MODE_CHOICES = [
        ('rr', 'Round Robin'),
        ('se', 'Single Elimination'),
        ('de', 'Double Elimination'),
    ]
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    mode = models.CharField(max_length=2, choices=MODE_CHOICES, default='rr')

    def __str__(self):
        return self.name

class Registration(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.tournament) + str(self.participant)