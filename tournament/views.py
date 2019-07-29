from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, ListView
from .models import Tournament, Registration, Bracket, Match1vs1
from .forms import NewTournamentForm, MatchResultForm
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
import datetime

def tournamentdetail(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    return render(request, 'tournament/details.html', {'tournament': tournament})

def tournament_new(request):
    if request.method == "POST":
        form = NewTournamentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect('tournament-detail', tournament_id=post.pk)
    else:
        form = NewTournamentForm()
    return render(request, 'tournament/new.html', {'form': form})


def showbracket(request, tournament_id):

    tournament = Tournament.objects.get(pk=tournament_id)
    bracket = Bracket.objects.get(tournament=tournament)

    if request.method == "POST":
        matchID = request.POST.get("matchID", "")
        winner = request.POST.get("winner", "")
        print("matchID" + matchID)
        print("winner" + winner)
        match = Match1vs1.objects.get(pk=matchID)
        match.set_winner(winner)
        match_list = Match1vs1.objects.filter(bracket=bracket).order_by('pk')
        matches = bracket.generate_bracket(match_list)
    else:
        matches = bracket.initiate_bracket()

    return render(request, 'tournament/bracket.html',
                      {'tournament': tournament, 'matches': matches,})


def showseeding(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    registrations = Registration.objects.filter(tournament=tournament_id)
    return render(request, 'tournament/seeding.html',
                  {'tournament': tournament, 'registrations': registrations})

def showparticipants(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    registrations = Registration.objects.filter(tournament=tournament_id)
    return render(request, 'tournament/participants.html',
                  {'tournament': tournament, 'registrations': registrations})


class TournamentsByEventListView(LoginRequiredMixin, ListView):
    model = Tournament
    template_name = 'accounts/tournamentlist.html'
    paginate_by = 10

    def get_queryset(self):
        return Tournament.objects.filter(event=self.request.event).order_by('name')