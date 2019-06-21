from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from .models import Event, Tournament
from .forms import NewEventForm
from django.shortcuts import redirect
from django.utils import timezone


def index(request):
    return HttpResponse("Hello, world. You're at the tourney index.")

def detail(request, event_id):
    return render(request, 'event/event-details.html', {'id': event_id})

def new(request):
    event_id = '3'
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
    return HttpResponse("You're looking at Tournament %s." % tournament_id)


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