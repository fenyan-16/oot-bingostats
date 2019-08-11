from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, ListView
from .models import Tournament, Registration, Bracket, Match1vs1, Team, RegistrationTeam, Result, User, Standing
from leagues.models import TournamentsInLeague, League
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
    start_date: datetime,
    registration_end_date: datetime,
    format: int,
    team_format: int,
    team_creation_mode: int
) -> Tournament:
    tournament = Tournament(owner=owner, name=name, description=description, max_participants=max_participants,
                            start_date=start_date, registration_end_date=registration_end_date,
                            format=format, team_format=team_format, team_creation_mode=team_creation_mode)

    tournament.save()

    # add_tournament_in_league(tournament=tournament, league=league)
    return (tournament)

def create_standing(
    tournament: Tournament,
    user: User,
    result: str
) -> Standing:
    standing = Standing(tournament=tournament, user=user, result=result)

    standing.save()

    # add_tournament_in_league(tournament=tournament, league=league)
    return (standing)

def add_tournament_in_league(
    tournament: Tournament,
    league: League,
) -> TournamentsInLeague:
    tournamentInLeague = TournamentsInLeague(tournament=tournament, league=league)

    tournamentInLeague.save()