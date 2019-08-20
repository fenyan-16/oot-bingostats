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
    max_participants = models.IntegerField(null=True)
    start_date = models.DateTimeField(null=True)
    registration_end_date = models.DateTimeField(null=True)

    format = models.IntegerField(null=True)

    team_format = models.IntegerField(null=True, default='1')


    team_creation_mode = models.IntegerField(null=True, default='1')

    # 1 = in creation, 2 = started, 0 = finished
    status = models.IntegerField(null=True, default='1')

    entrant_list = {'Fenyan', 'Malouna', 'Mitsuhito', 'Celthar', 'Souldes', 'Florin', 'Neas', 'Narrow', 'Duanos',
                    'Aquilion'}
    seeds = {5, 3, 2, 7, 1, 8, 9, 4, 6, 10}

    def find_registration(self, user):
        registrations = RegistrationTeam.objects.filter(tournament=self)
        for registration in registrations:
            if registration.team.player1 == user or registration.team.player2 == user or registration.team.player3 == user or registration.team.player4 == user or registration.team.player5 == user or registration.team.player6 == user:
                return registration
        return False

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
    MODE_CHOICES = [
        ('rr', 'Round Robin'),
        ('se', 'Single Elimination'),
        ('de', 'Double Elimination'),
    ]
    mode = models.CharField(max_length=2, choices=MODE_CHOICES, default='se')

    def initiate_bracket(self, mode='Distance'):
        print("hello")
        self.delete_matches()
        seeds = [5, 3, 2, 7, 1, 8, 9, 4, 6, 10]
        bracket_level_matches = list()
        depth = 3

        registrations = Registration.objects.filter(tournament=self.tournament)
        # _, registrations = (list(s) for s in zip(*sorted(zip([p.seed for p in registrations], registrations))))

        # seeds, entrants = (list(s) for s in zip(*sorted(zip([p.seed for p in registrations], [p.participant for p in registrations]))))


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

        for registration in registrations:
            print(registration)

        print(self.distance_seeds(len(seeds)))
        # fill first depth_level matches
        this_levels_matches = list()
        for s1, s2 in zip(seeds[::2], seeds[1::2]):

            try:
                player1 = registrations[s1 - 1].participant
            except IndexError:
                player1 = None

            try:
                player2 = registrations[s2 - 1].participant
            except IndexError:
                player2 = None

            this_depth_level = 0;
            if (player1 is None) or (player2 is None):
                if (player2 is None):
                    new_match = Match1vs1(bracket=self, depth_level=this_depth_level, player1=player1, player2=player2,
                                      bye_flag=True,
                                      planned=True, player1_result=None, player2_result=None, played=True, winner=1)
                else:
                    new_match = Match1vs1(bracket=self, depth_level=this_depth_level, player1=player1, player2=player2,
                                      bye_flag=True, planned=True, winner=2)
            else:
                new_match = Match1vs1(bracket=self, depth_level=this_depth_level, player1=player1, player2=player2,
                                  bye_flag=False, planned=True, winner=0)
            new_match.save()
            this_levels_matches.append(new_match)


        bracket_level_matches.append(this_levels_matches)
        print("match list: " + str(bracket_level_matches))

        # fill matches for depth_level > 0

        for level in np.arange(1, depth):
            this_levels_matches = list()
            for _ in np.arange(2 ** (depth - level - 1)):
                this_match = Match1vs1(bracket=self, depth_level=level, player1=None, player2=None, bye_flag=False,
                                   planned=False, player1_result=None, player2_result=None, played=False, winner=0)

                this_match.save()
                this_levels_matches.append(this_match)
            bracket_level_matches.append(this_levels_matches)

        # print("full match list: " + str(bracket_level_matches))
        return (bracket_level_matches)

    def distance_seeds(self, list_length):
        seeds = [1]
        while len(seeds) < list_length:
            games = zip(seeds, (2 * len(seeds) + 1 - seed for seed in seeds))
            seeds = [team for game in games for team in game]
        return seeds

    def generate_bracket(self, match_list):
        depth = 3
        bracket_level_matches = list()

        for level in np.arange(0, depth):
            this_levels_matches = list()
            for match in match_list:
                if match.depth_level == level:
                    this_levels_matches.append(match)
            bracket_level_matches.append(this_levels_matches)
            print("full match list: " + str(this_levels_matches))
        return (bracket_level_matches)

    def set_winner_and_propagate(self, winner, match_id):
        match = Match1vs1.objects.get(pk=match_id)
        match.set_winner(winner)

        match_qs = Match1vs1.objects.filter(bracket=self.pk).order_by('pk')
        match_list = list(match_qs)
        match_id_in_bracket = match_list.index(match)

        # 3 durch depth austauschen
        propagation_match_id = (match_id_in_bracket + 2 ** 3 + 1) / 2 - 1
        if np.mod(propagation_match_id, 1) > 0:
            winner_position = 1
        else:
            winner_position = 2
        print("match" + str(propagation_match_id))
        print("slot" + str(winner_position))

        propagation_match_id = int(np.ceil(propagation_match_id))
        propagation_match = match_list[propagation_match_id]
        print(propagation_match)

        if match.winner == 1:
            match_winner = match.player1
        elif match.winner == 2:
            match_winner = match.player2
        else:
            print('Invalid')

        if winner_position == 1:
            propagation_match.player1 = match_winner
        elif winner_position == 2:
            propagation_match.player2 = match_winner
        else:
            print('Invalid')

        propagation_match.save()

    def delete_matches(self):
        match_list = Match1vs1.objects.filter(bracket=self.pk)
        for match in match_list:
            match.delete()

    def __str__(self):
        return str(self.pk)


class Match1vs1(models.Model):
    player1 = models.ForeignKey(User, related_name='player_one', on_delete=models.CASCADE, null=True)
    player2 = models.ForeignKey(User, related_name='player_two', on_delete=models.CASCADE, null=True)
    player1_result = models.DecimalField(decimal_places=2, max_digits=3, null=True)
    player2_result = models.DecimalField(decimal_places=2, max_digits=3, null=True)
    depth_level = models.IntegerField(null=True)
    bye_flag = models.BooleanField(null=True)
    planned = models.BooleanField(null=True)
    played = models.BooleanField(null=True)
    winner = models.IntegerField(null=True)
    bracket = models.ForeignKey(Bracket, on_delete=models.CASCADE)

    def set_winner(self, winner):
        self.winner = winner
        self.played = True
        self.planned = False
        self.save()

    def __str__(self):
        return str(self.player1) + str(self.player2)


class MatchTeam(models.Model):
    team1 = models.ForeignKey(User, related_name='team_one', on_delete=models.CASCADE, null=True)
    team2 = models.ForeignKey(User, related_name='team_two', on_delete=models.CASCADE, null=True)
    team1_result = models.DecimalField(decimal_places=2, max_digits=3, null=True)
    team2_result = models.DecimalField(decimal_places=2, max_digits=3, null=True)
    depth_level = models.IntegerField(null=True)
    bye_flag = models.BooleanField(null=True)
    planned = models.BooleanField(null=True)
    played = models.BooleanField(null=True)
    winner = models.IntegerField(null=True)
    bracket = models.ForeignKey(Bracket, on_delete=models.CASCADE)

    def set_winner(self, winner):
        self.winner = winner
        self.played = True
        self.planned = False
        self.save()

    def __str__(self):
        return str(self.player1) + str(self.player2)


class Team(models.Model):
    player1 = models.ForeignKey(User, related_name='team_player_one', on_delete=models.CASCADE, null=True)
    player2 = models.ForeignKey(User, related_name='team_player_two', on_delete=models.CASCADE, null=True)
    player3 = models.ForeignKey(User, related_name='team_player_three', on_delete=models.CASCADE, null=True)
    player4 = models.ForeignKey(User, related_name='team_player_four', on_delete=models.CASCADE, null=True)
    player5 = models.ForeignKey(User, related_name='team_player_five', on_delete=models.CASCADE, null=True)
    player6 = models.ForeignKey(User, related_name='team_player_six', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    member_count = models.IntegerField(null=True)

    def __str__(self):
        return str(self.name)


class RegistrationTeam(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    seed = models.IntegerFielddepth_level = models.IntegerField(null=True)

    def __str__(self):
        return str(self.tournament) + str(self.team)

# Löschen
class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    place = models.IntegerField(null=True)
    score = models.TimeField(null=True)

    def __str__(self):
        return str(self.user) + str(self.tournament)


class Standing(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    placement = models.IntegerField(null=True)
    result = models.DurationField(max_length=64, null=True)

    def __str__(self):
        return str(self.tournament) + str(self.placement) + str(self.user)