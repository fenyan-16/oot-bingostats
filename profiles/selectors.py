from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, ListView
from tournament.models import Tournament, Registration, Bracket, Match1vs1, Team, RegistrationTeam, Standing
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
import datetime

def get_latest_results(*, user):
    all_latest_results = Standing.objects.filter(user=user)

    return all_latest_results


def league_positions(*, league_id):
    latest_ten_results = Tournament.objects.filter(pk=league_id)
    all_results = Standing.objects.filter(tournament=league_id)

    return all_results


class TournamentsByEventListView(LoginRequiredMixin, ListView):
    model = Tournament
    template_name = 'accounts/tournamentlist.html'
    paginate_by = 10

    def get_queryset(self):
        return Tournament.objects.filter(event=self.request.event).order_by('name')
