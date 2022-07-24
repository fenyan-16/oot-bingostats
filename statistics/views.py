from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, ListView
from django.forms import formset_factory, modelformset_factory
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template import RequestContext
from .services import return_goallist, return_playerstats, return_goal_combinations, return_race_count, return_timestamp


def goals(request, year, phase):
	goal_df_repr = return_goallist(phase, year=year)
	total_races = return_race_count(phase, year=year)
	timestamp = return_timestamp(phase, year)

	return render(request, 'goals.html', {'goals': goal_df_repr, 'racecount': total_races,
	                                      'year': year, 'timestamp': timestamp})


def players(request, year, phase):
	player_df_repr = return_playerstats(phase, year=year)
	timestamp = return_timestamp(phase, year)

	return render(request, 'players.html', {'players': player_df_repr, 'year': year, 'timestamp': timestamp})


def combinations(request, year):
	goal_combi_repr = return_goal_combinations(year=year)
	total_races = return_race_count(year=year, mode='swiss')+return_race_count(year=year, mode='top16')
	timestamp = return_timestamp('swiss', year)

	return render(request, 'combinations.html', {'combinations': goal_combi_repr, 'racecount': total_races, 'year': year
	                                             , 'timestamp': timestamp})


def frequency(request):
	return render(request, 'frequency.html')


def players_era(request):
	player_df_repr = return_playerstats('swiss', year='v10.1')
	timestamp = return_timestamp('', 'v10.1')
	return render(request, 'players_era.html', {'players': player_df_repr, 'timestamp': timestamp})


def goals_era(request, year):
	goal_df_repr = return_goallist('swiss', year=year)
	total_races = return_race_count('swiss', year=year)
	timestamp = return_timestamp('', year)

	return render(request, 'goals_era.html', {'goals': goal_df_repr, 'racecount': total_races, 'timestamp': timestamp})


def combinations_era(request):
	goal_combi_repr = return_goal_combinations(year='v10.1')
	total_races = return_race_count(year='v10.1', mode='swiss')
	timestamp = return_timestamp('', 'v10.1')

	return render(request, 'combinations_era.html', {'combinations': goal_combi_repr, 'racecount': total_races, 'timestamp': timestamp})
