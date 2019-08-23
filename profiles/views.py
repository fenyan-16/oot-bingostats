from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, ListView
from django.forms import formset_factory, modelformset_factory
from .forms import EditProfileForm, CreateUserForm
from .models import Userprofile
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template import RequestContext
import datetime
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        form = CreateUserForm()
    return render(request, 'registration/signup.html', {'form': form})

def profile_edit(request, user_id):
    profile = Userprofile.objects.get(pk=user_id)

    if request.method == "POST":
        form = EditProfileForm(request.POST)
        if form.is_valid():

            return render(request, 'profile/details.html', {'profile': profile})
    else:
        form = EditProfileForm()
    return render(request, 'profile/new.html', {'form': form})


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        profile_form = EditProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid() and profile_form.is_valid():
            profile_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        profile_form = EditProfileForm()
    return render(request, 'accounts/edit.html', {
        'user_form': profile_form,
        'profile_form': profile_form
    })

def profile_detail(request, user_id):
    profile = Userprofile.objects.get(pk=user_id)

    return render(request, 'profile/details.html', {'profile': profile})


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if (user is not None and default_token_generator.check_token(user, token)):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.INFO, 'Account activated. Please login.')
    else:
        messages.add_message(request, messages.INFO, 'Link Expired. Contact admin to activate your account.')

    return redirect('djangobin:login')
