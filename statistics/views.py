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
from .services import return_goallist, return_playerstats


def goals(request):
	goal_df_repr = return_goallist()

	return render(request, 'goals.html', {'goals': goal_df_repr})


def players(request):
	player_df_repr = return_playerstats()

	return render(request, 'players.html', {'players': player_df_repr})
