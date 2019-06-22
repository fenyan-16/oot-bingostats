from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from .models import Event, Tournament
from .forms import NewEventForm, NewTournamentForm
from django.shortcuts import redirect
from django.utils import timezone


def index(request):
    return render(request, 'index.html')

def eventlist(request):
    return HttpResponse("Eventliste")

def event_detail(request, event_id):
    return render(request, 'event/event-details.html', {'id': event_id})

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

def tournamentdetail(request, event_id, tournament_id):
    return render(request, 'tournament/details.html', {'id': event_id})


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