from django.db import models
from django.contrib.auth.models import User
import numpy as np
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField


# Create your models here.

class Tournament(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, null=True)
    name = models.CharField(max_length=200)

    entrant_list = {'Fenyan', 'Malouna', 'Mitsuhito', 'Celthar', 'Souldes', 'Florin', 'Neas', 'Narrow', 'Duanos',
                    'Aquilion'}
    seeds = {5, 3, 2, 7, 1, 8, 9, 4, 6, 10}

    def __str__(self):
        return self.name


class Registration(models.Model):
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    seed = models.IntegerField(null=True)

    def __str__(self):
        return str(self.tournament) + str(self.participant)


class Bracket(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    def generate_bracket(self, mode='Distance'):
        depth = 2

        registrations = Registration.objects.filter(pk=self.tournament.pk)
        _, registrations = (list(s) for s in zip(*sorted(zip([p.seed for p in registrations], registrations))))

        seeds, entrants = (list(s) for s in zip(*sorted(zip([p.seed for p in registrations], [p.participant for p in registrations]))))


        round = 0
        round_width = int(2 ** depth)
        # wie füllen wir null (buy) matches aus
        # while len(registrations) < round_width:
        #     registrations.append(Registration())
        match_counter = 1
        if mode == 'Distance':
            seeds = self.distance_seeds(len(registrations))
        elif mode == 'TopDown':
            seeds = sorted(seeds)
            seeds.extend(np.arange(np.max(seeds) + 1, round_width))
        elif mode == 'Entered':
            seeds.extend(np.arange(np.max(seeds) + 1, round_width))
        elif mode == 'Random':
            import random
            seeds.extend(np.arange(np.max(seeds) + 1, round_width))
            random.shuffle(seeds)

        for s1, s2 in zip(seeds[::2], seeds[1::2]):

            try:
                player1 = registrations[s1 - 1]
            except IndexError:
                player1 = None

            try:
                player2 = registrations[s2 - 1]
            except IndexError:
                player2 = None

            if (player1 is None) or (player2 is None):
                if (player2 is None):
                    new_match = Match(depth_level=0, player1=player1, player2=player2, bye_flag=True,
                                      planned=True, player1_result=None, player2_result=None, played=True)
                else:
                    new_match = Match(depth_level=0, player1=player1, player2=player2, bye_flag=True, planned=True)
            else:
                new_match = Match(depth_level=0, player1=player1, player2=player2, bye_flag=False, planned=True)
            new_match.save()

            match_counter += 1

        # for level in np.arange(1, self.depth):
        #     this_levels_matches = list()
        #     for _ in np.arange(2 ** (self.depth - level - 1)):
        #         this_match = Match(match_counter, int(level))
        #         this_levels_matches.append(this_match)
        #         self.match_list.append(this_match)
        #         match_counter += 1
        #     self.bracket_levels.append(this_levels_matches)

    def distance_seeds(self, list_length):
        seeds = [1]
        while len(seeds) < list_length:
            games = zip(seeds, (2 * len(seeds) + 1 - seed for seed in seeds))
            seeds = [team for game in games for team in game]
        return seeds

    def __str__(self):
        return str(self.pk)


class Match(models.Model):
    player1 = models.ForeignKey(User, related_name='player_one', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='player_two', on_delete=models.CASCADE)
    player1_result = models.DecimalField(decimal_places=2, max_digits=3, null=True)
    player2_result = models.DecimalField(decimal_places=2, max_digits=3, null=True)
    depth_level = models.IntegerField(null=True)
    bye_flag = models.BooleanField(null=True)
    planned = models.BooleanField(null=True)
    played = models.BooleanField(null=True)

    def __str__(self):
        return self.pk
