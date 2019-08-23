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
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Userprofile

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


@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def update_user_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Userprofile.objects.create(owner=user)
        profile.save()


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.profile.email_confirmed)
        )
