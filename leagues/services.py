from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, ListView
from .models import TournamentsInLeague, User, League, Ratingpoints
from tournament.models import Tournament, Standing
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
import datetime

def create_league(
    owner: User,
    name: str,
    description: str,
    start_date: datetime,
    end_date: datetime,
) -> League:
    league = League(owner=owner, name=name, description=description, start_date=start_date, end_date=end_date)
    league.save()

    return (league)

def create_ranting_points(
    league: League,
    tournament: Tournament,
    user: User,
    points: int
) -> Ratingpoints:
    rating = Ratingpoints(league=league, tournament=tournament, user=user, points=points)
    rating.save()


def add_tournament_in_league(
    tournament: Tournament,
    league: League,
) -> TournamentsInLeague:
    tournamentInLeague = TournamentsInLeague(tournament=tournament, league=league)
    tournamentInLeague.save()


def get_tournaments_in_league(league_id: int):
    standings_list = list()
    league = League.objects.get(pk=league_id)
    # all Tournaments that belong this league
    tournamentsInLeague = TournamentsInLeague.objects.filter(league=league)
    for tournament in tournamentsInLeague:
        standings = Standing.objects.filter(tournament=tournament.tournament)
        standings_list.append(standings)
        print(standings)
    return(standings_list)