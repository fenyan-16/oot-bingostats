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
from .forms import EditProfileForm, CreateUserForm, LoginForm
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
from django.template.loader import render_to_string
from .services import AccountActivationTokenGenerator, get_my_latest_results
from django.contrib.sites.shortcuts import get_current_site

def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            account_activation_token = AccountActivationTokenGenerator()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('email/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return render(request, 'registration/account_activation.html')
    else:
        form = CreateUserForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    account_activation_token = AccountActivationTokenGenerator()
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('login')
    else:
        return render(request, 'account_activation_invalid.html')


def account_activation_sent(request):
    return render(request, 'signup')

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
    user = User.objects.get(pk=user_id)
    profile = Userprofile.objects.get(owner=user)

    result_list, leagueinfo_list = get_my_latest_results(user_id)

    zipped_results_and_league = zip(result_list, leagueinfo_list)

    return render(request, 'accounts/profile.html', {'profile': profile, 'zipped_results_and_league': zipped_results_and_league})

def profile_detail_name(request, user_name):
    user = User.objects.get(username=user_name)
    profile = Userprofile.objects.get(owner=user)

    result_list, leagueinfo_list = get_my_latest_results(user.pk)

    zipped_results_and_league = zip(result_list, leagueinfo_list)

    return render(request, 'accounts/profile.html', {'profile': profile, 'zipped_results_and_league': zipped_results_and_league})


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


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                # Is the account active? It could have been disabled.
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponse("xxx.")
            else:
                # Bad login details were provided. So we can't log the user in.
                print("Invalid login details: {0}, {1}".format(username, password))
                return HttpResponse("Invalid login details supplied.")
        else:
            return HttpResponse("Logged in.")
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})