from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, ListView
from .models import Tournament, Registration, Bracket, Match1vs1, Team, RegistrationTeam, Result, User, Standing, Game
from leagues.models import TournamentsInLeague, League, Ratingpoints
from leagues.services import create_ranting_points
from datetime import timedelta
from .forms import NewTournamentForm, NewBracketForm
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
import datetime

def create_tournament(
    owner: User,
    name: str,
    description: str,
    max_participants: int,
    date: datetime,
    format: int,
    team_format: int,
    team_creation_mode: int,
    game: Game
) -> Tournament:
    tournament = Tournament(owner=owner, name=name, description=description, max_participants=max_participants,
                            date=date, format=format, team_format=team_format, team_creation_mode=team_creation_mode,
                            game=game)

    tournament.save()

    # add_tournament_in_league(tournament=tournament, league=league)
    return (tournament)

def create_standing(
    tournament: Tournament,
    user: User,
    result: timedelta
) -> Standing:
    try:
        standing = Standing.objects.get(tournament=tournament, user=user)
        return False
    except:
        standing = Standing(tournament=tournament, user=user, result=result)
        standing.save()
        return True


def delete_standing(tournament: Tournament, user: User):
    Standing.objects.filter(tournament=tournament, user=user).delete()


def add_tournament_in_league(
    tournament: Tournament,
    league: League,
) -> TournamentsInLeague:
    tournamentInLeague = TournamentsInLeague(tournament=tournament, league=league)

    tournamentInLeague.save()


def finish_tournament(tournament: Tournament):
    tournament.status = 0
    tournament.save()
    standings = Standing.objects.filter(tournament=tournament).order_by('result')
    leagues_for_tournament = TournamentsInLeague.objects.filter(tournament=tournament)

    rankingpoints = [100, 85, 70, 60, 50, 42, 35, 30, 25, 20, 15, 12, 10, 8, 7, 6, 6, 5, 5, 5]

    for count, standing in enumerate(standings):
        standing.placement = count+1
        standing.save()
        for league in leagues_for_tournament:
            create_ranting_points(league=league.league, tournament=tournament, user=standing.user, points=rankingpoints[count])

    return(tournament)


def get_standings_and_leaguepoints(tournament: Tournament):
    standings_and_leaguepoints = list()

    standings = Standing.objects.filter(tournament=tournament).order_by('result')
    leagues_for_tournament = TournamentsInLeague.objects.filter(tournament=tournament)

    if (tournament.status == 0):
        for standing in standings:
            row = list()
            row.append(standing.placement)
            row.append(standing.user)
            row.append(standing.result)
            for league in leagues_for_tournament:
                ratingpoints = Ratingpoints.objects.get(league=league.league, tournament=tournament, user=standing.user)
                row.append(ratingpoints.points)
            standings_and_leaguepoints.append(row)


    else:
        standings_and_leaguepoints = None
    return (standings_and_leaguepoints)


def reopen_tournament(tournament: Tournament):
    tournament.status = 1
    tournament.save()
    Ratingpoints.objects.filter(tournament=tournament).delete()
