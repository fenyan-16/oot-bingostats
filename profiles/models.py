from django.db import models
from django.contrib.auth.models import User
import numpy as np
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Userprofile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userdata')
    email_confirmed = models.BooleanField(default=False)
    twitch_username = models.CharField(max_length=100, null=True, blank=True)
    twitter_username = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.owner)
