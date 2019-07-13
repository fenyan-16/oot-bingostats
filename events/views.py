from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, ListView
from .models import Event, Phase
from .forms import NewEventForm, NewPhaseForm, UserForm, ProfileForm
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages


def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def eventlist(request):
    return HttpResponse("Eventliste")

def event_detail(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'event/event-details.html', {'event': event})

def event_new(request):
    if request.method == "POST":
        form = NewEventForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.pub_date = timezone.now()
            post.save()
            return redirect('detail', event_id=post.pk)
    else:
        form = NewEventForm()
    return render(request, 'event/new.html', {'form': form})

def event_edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == "POST":
        form = NewEventForm(request.POST, instance=event)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect('detail', event_id=post.pk)
    else:
        form = NewEventForm(instance=event)
    return render(request, 'event/edit.html', {'form': form})


def event_registration_status (request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'event/registration-status.html', {'event': event})

def tournamentdetail(request, event_id, tournament_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'tournament/details.html', {'event': event})

def myevents(request):
    event_list = Event.objects.filter(owner=request.user.pk)
    return render(request, 'accounts/myevents.html', {'event_list': event_list})

def tournament_seeding(request, event_id, tournament_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'tournament/seeding.html',
                  {'event': event})

def phase_new(request, event_id, tournament_id):
    if request.method == "POST":
        form = NewPhaseForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('tournament-detail', event_id=event_id)
    else:
        form = NewPhaseForm()
    return render(request, 'phase/new.html', {'form': form})

class EventsByUserListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'accounts/myevents.html'
    paginate_by = 10

    def get_queryset(self):
        return Event.objects.filter(owner=self.request.user).order_by('name')