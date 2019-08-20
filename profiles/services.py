from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, ListView
from leagues.models import TournamentsInLeague, League, Ratingpoints
from .models import Userprofile
from django.contrib.auth.models import User
from tournament.models import Tournament, Standing
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
import datetime

def create_userprofile(
    owner: User,
    name: str,
    description: str,
    start_date: datetime,
    end_date: datetime,
) -> Userprofile:
    league = League(owner=owner, name=name, description=description, start_date=start_date, end_date=end_date)
    league.save()

    return (league)