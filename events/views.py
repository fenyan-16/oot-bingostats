from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, ListView
from .models import Event, Tournament, Registration, Phase
from .forms import NewEventForm, NewTournamentForm, NewPhaseForm, EventRegistrationForm
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone


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

def eventlist(request):
    return HttpResponse("Eventliste")

def event_detail(request, event_id):
    event = Event.objects.get(pk=event_id)
    tournaments = Tournament.objects.filter(event=event_id)
    return render(request, 'event/event-details.html', {'event': event, 'tournaments': tournaments})

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

def event_register(request, event_id):
    event = Event.objects.get(pk=event_id)
    tournaments = Tournament.objects.filter(event=event_id)

    if request.method == "POST":
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            for tournament in tournaments:
                post = form.save(commit=False)
                post.tournament = tournament
                post.participant = request.user
                post.save()
            return redirect('detail', event_id=post.pk)
    else:
        form = EventRegistrationForm()
    return render(request, 'event/registration.html', {'event': event, 'tournaments': tournaments, 'form': form})

def event_registration_status (request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'event/registration-status.html', {'event': event})

def tournamentdetail(request, event_id, tournament_id):
    event = Event.objects.get(pk=event_id)
    tournament = Tournament.objects.get(pk=tournament_id)
    phases = Phase.objects.filter(tournament=tournament)
    registrations = Registration.objects.filter(tournament=tournament)
    return render(request, 'tournament/details.html', {'event': event, 'tournament': tournament, 'phases': phases, 'registrations': registrations})

def myevents(request):
    event_list = Event.objects.filter(owner=request.user.pk)
    return render(request, 'accounts/myevents.html', {'event_list': event_list})

def tournament_new(request, event_id):
    if request.method == "POST":
        form = NewTournamentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.event = Event.objects.get(pk=event_id)
            post.save()
            return redirect('tournament-detail', event_id=event_id, tournament_id=post.pk)
    else:
        form = NewTournamentForm()
    return render(request, 'tournament/new.html', {'form': form})

def phase_new(request, event_id, tournament_id):
    if request.method == "POST":
        form = NewPhaseForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.tournament = Tournament.objects.get(pk=tournament_id)
            post.save()
            return redirect('tournament-detail', event_id=event_id, tournament_id=tournament_id)
    else:
        form = NewPhaseForm()
    return render(request, 'phase/new.html', {'form': form})

class EventsByUserListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'accounts/myevents.html'
    paginate_by = 10

    def get_queryset(self):
        return Event.objects.filter(owner=self.request.user).order_by('name')

class TournamentsByEventListView(LoginRequiredMixin, ListView):
    model = Tournament
    template_name = 'accounts/tournamentlist.html'
    paginate_by = 10

    def get_queryset(self):
        return Tournament.objects.filter(event=self.request.event).order_by('name')