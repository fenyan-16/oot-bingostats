from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, ListView
from django.forms import formset_factory, modelformset_factory
from .models import Tournament, Registration, Bracket, Match1vs1, Team, RegistrationTeam, League
from .forms import NewTournamentForm, NewBracketForm, TournamentsInLeague, LeagueForm
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect
from .services import create_tournament, add_tournament_in_league
from django.template import RequestContext
import datetime

def tournamentdetail(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    actual_participants = RegistrationTeam.objects.filter(tournament=tournament).count()
    registrations = RegistrationTeam.objects.filter(tournament=tournament)
    regisered = False
    user_registration = tournament.find_registration(request.user)

    if user_registration:
        regisered = True
    if request.method == "POST":
        if tournament.format > 1:
            if request.method == "POST":
                teamname_create = request.POST.get("teamname_create", "")
                print(str(teamname_create))
                new_team = Team(name=teamname_create, player1=request.user, member_count=tournament.format)
                new_team.save()
                new_registration = RegistrationTeam(team=new_team, tournament=tournament, seed=0)
                new_registration.save()
        else:
            if Registration.objects.filter(tournament=tournament, participant=request.user):
                messages.warning(request, "You already registered for " + tournament.name)
            else:
                registration = Registration(tournament=tournament, participant=request.user, seed=0)
                registration.save()
                messages.info(request, "You successfully registered for " + tournament.name)
    return render(request, 'tournament/details.html', {'tournament': tournament, 'registrations': registrations, 'user_registration': user_registration})


def tournament_new(request):
    tournament_instance = Tournament()

    if request.method == "POST":
        if request.POST['action'] == "+":
            extra = int(request.POST['extra']) + 1
            leagueFormSet = formset_factory(LeagueForm, extra=extra)

            tournament_form = NewTournamentForm(request.POST)

        else:
            extra = int(float(request.POST['extra']))
            leagueFormSet = formset_factory(LeagueForm, extra=extra)(request.POST)
            tournament_form = NewTournamentForm(request.POST)

            if tournament_form.is_valid():
                tournament_instance = create_tournament(request.user, tournament_form.cleaned_data['name'], tournament_form.cleaned_data['description'],
                                                     tournament_form.cleaned_data['max_participants'], tournament_form.cleaned_data['start_date'],
                                                     tournament_form.cleaned_data['registration_end_date'], tournament_form.cleaned_data['format'],
                                                     tournament_form.cleaned_data['team_creation_mode'])
                for i in range(int(request.POST['extra'])):
                    league_field = 'form-' + str(i) + '-league'
                    print(league_field)
                    add_tournament_in_league(tournament_instance, League.objects.get(pk=request.POST[league_field]))
            return redirect('tournament-detail', tournament_id=tournament_instance.pk)
    else:
        tournament_form = NewTournamentForm()
        leagueFormSet = formset_factory(LeagueForm, extra=1)
        return render(request, 'tournament/new.html', {'tournament_form': tournament_form, 'leagueForms': leagueFormSet, 'extra': 1})
    return render(request, 'tournament/new.html', {'tournament_form': tournament_form, 'leagueForms': leagueFormSet, 'extra': extra})


def showbracket(request, tournament_id):

    tournament = Tournament.objects.get(pk=tournament_id)
    bracket = Bracket.objects.get(tournament=tournament)

    if request.method == "POST":
        match_id = request.POST.get("matchID", "")
        winner = int(request.POST.get("winner", ""))
        print("matchID" + match_id)
        print("winner" + str(winner))
        bracket.set_winner_and_propagate(winner, match_id)

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


def bracket_new(request, tournament_id):
    if request.method == "POST":
        form = NewBracketForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.mode = request.mode
            post.tournament = Tournament.objects.get(pk=tournament_id)
            post.save()
            return redirect('bracket', tournament_id=post.pk)
    else:
        form = NewBracketForm()
    return render(request, 'bracket/new.html', {'form': form})


def league(request):
    form = TournamentsInLeague(request.POST)
    return render(request, 'bracket/new.html', {'form': form})


def some_view(request):
    if request.method == 'POST':
        if request.POST['action'] == "+":
            extra = int(2) + 1
            form = NewTournamentForm(initial=request.POST)
            formset = formset_factory(FormsetForm, extra=extra)
        else:
            extra = int(float(request.POST['extra']))
            form = NewTournamentForm(request.POST)
            formset = formset_factory(FormsetForm, extra=extra)(request.POST)

            if form.is_valid() and formset.is_valid():
                if request.POST['action'] == "Create":
                    for form_c in formset:
                        if not form_c.cleaned_data['delete']:
                            # create data
                            data=list()
                elif request.POST['action'] == "Edit":
                    for form_c in formset:
                        if form_c.cleaned_data['delete']:
                            # delete data
                            data=list()
                        else:
                            # create data
                            data=list()
                return HttpResponseRedirect('tournament-new')
    form = NewTournamentForm()
    extra = 1
    formset = formset_factory(FormsetForm, extra=extra)

    return render(request, 'tournament/new2.html', {'form': form, 'add_league_form': formset})
