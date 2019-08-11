from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, ListView
from django.forms import formset_factory, modelformset_factory
from .models import League, TournamentsInLeague
from .forms import NewLeagueForm
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect
from .services import create_league, add_tournament_in_league, get_tournaments_in_league
from django.template import RequestContext
import datetime


def league_list(request):
    leagues = League.objects.all()

    return render(request, 'league/list.html', {'leagues': leagues})

def league_new(request):
    if request.method == "POST":
        form = NewLeagueForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            league = create_league(request.user, form.cleaned_data['name'], form.cleaned_data['description'],
                                    form.cleaned_data['start_date'], form.cleaned_data['registration_end_date'])


            return redirect('league-details', league_id=league.pk)
    else:
        form = NewLeagueForm()
    return render(request, 'league/new.html', {'form': form})


def league_detail(request, league_id):
    league = League.objects.get(pk=league_id)
    tournament_standings = get_tournaments_in_league(league_id)

    return render(request, 'league/details.html', {'league': league, 'tournament_standings': tournament_standings})
