from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django import template
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, ListView
from leagues.models import TournamentsInLeague, League, Ratingpoints
from profiles.models import Userprofile
from django.contrib.auth.models import User
from tournament.models import Tournament, Standing
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
import datetime
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils import six
from django.dispatch import receiver
from django.db.models.signals import post_save
from profiles.models import Userprofile

register = template.Library()
@register.filter(name='zip')
def zip_list(a, b):
    return zip(a, b)