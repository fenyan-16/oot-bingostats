from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Tournament(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, null=True)
    name = models.CharField(max_length=200)

    entrant_list = {'Fenyan', 'Malouna', 'Mitsuhito', 'Celthar', 'Souldes', 'Florin', 'Neas', 'Narrow', 'Duanos', 'Aquilion'}
    seeds = {5, 3, 2, 7, 1, 8, 9, 4, 6, 10}

    def __str__(self):
        return self.name

class Registration(models.Model):
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.tournament) + str(self.participant)

class Bracket(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    def __str__(self):
        return self.pk


class Match(models.Model):
	player1 = models.ForeignKey(User, on_delete=models.CASCADE)
	player2 = models.ForeignKey(User, on_delete=models.CASCADE)
	player1_result = models.DecimalField(decimal_places=2, max_digits=3, null=True)
	player2_result = models.DecimalField(decimal_places=2, max_digits=3, null=True)

	def __str__(self):
		return self.pk