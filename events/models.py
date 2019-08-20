from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .bracket import Bracket, Entrant
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

class Phase(models.Model):
    MODE_CHOICES = [
        ('rr', 'Round Robin'),
        ('se', 'Single Elimination'),
        ('de', 'Double Elimination'),
    ]
    name = models.CharField(max_length=200)
    mode = models.CharField(max_length=2, choices=MODE_CHOICES, default='rr')

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()