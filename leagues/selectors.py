from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, ListView
from .models import Tournament, Registration, Bracket, Match1vs1, Team, RegistrationTeam, Result, TournamentsInLeague
from .forms import NewTournamentForm, NewBracketForm
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
import datetime

def get_results_for_leagues(*, league_id):
    tournaments_in_league = TournamentsInLeague.objects.filter(pk=league_id)
    all_results = Result.objects.filter(tournament=tournaments_in_league)

    return all_results


class TournamentsByEventListView(LoginRequiredMixin, ListView):
    model = Tournament
    template_name = 'accounts/tournamentlist.html'
    paginate_by = 10

    def get_queryset(self):
        return Tournament.objects.filter(event=self.request.event).order_by('name')
