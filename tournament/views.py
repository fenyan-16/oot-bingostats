from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, ListView
from django.forms import formset_factory, modelformset_factory
from .models import Tournament, Registration, Bracket, Match1vs1, Team, RegistrationTeam, Standing, Game
from leagues.models import League
from django.contrib.auth.models import User
from .forms import NewTournamentForm, NewBracketForm, LeagueForm, ReportStandingsForm
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect
from .services import create_tournament, add_tournament_in_league, create_standing, finish_tournament, get_standings_and_leaguepoints
from django.template import RequestContext
import datetime


def index(request):
    return render(request, 'index.html')

def tournament_list(request, format):
    if format == 'race':
        tournaments = Tournament.objects.filter(format='1').order_by('-date')
    else:
        tournaments = Tournament.objects.filter(format='0').order_by('-date')

    return render(request, 'tournament/list.html', {'tournaments': tournaments, 'format': format})


def tournament_detail_old(request, tournament_id):
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


def tournament_new(request, format):
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
            game = Game.objects.get(pk=2)

            if tournament_form.is_valid():
                if format == 0:
                    tournament_instance = create_tournament(request.user, tournament_form.cleaned_data['name'], tournament_form.cleaned_data['description'],
                                                            64, tournament_form.cleaned_data['date'],
                                                            0, 1, 1, game)
                else:
                    tournament_instance = create_tournament(request.user, tournament_form.cleaned_data['name'], tournament_form.cleaned_data['description'],
                                                            64, tournament_form.cleaned_data['date'],
                                                            1, 1, 1, game)
                for i in range(int(request.POST['extra'])):
                    league_field = 'form-' + str(i) + '-league'
                    print(league_field)
                    if request.POST[league_field]:
                        add_tournament_in_league(tournament_instance, League.objects.get(pk=request.POST[league_field]))
            return redirect('tournament-detail', tournament_id=tournament_instance.pk)
    else:
        tournament_form = NewTournamentForm()
        leagueFormSet = formset_factory(LeagueForm, extra=1)
        return render(request, 'tournament/new.html', {'tournament_form': tournament_form, 'leagueForms': leagueFormSet, 'extra': 1})
    return render(request, 'tournament/new.html', {'tournament_form': tournament_form, 'leagueForms': leagueFormSet, 'extra': extra})


def tournament_detail(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    report_form = ReportStandingsForm()

    if tournament.status == 0:
        standings = get_standings_and_leaguepoints(tournament)
        return render(request, 'tournament/details.html', {'tournament': tournament, 'standings': standings})
    else:
        if request.method == "POST":
            if request.POST['action'] == "save":
                user = User.objects.get(pk=request.POST['user'])
                standing_succeed = create_standing(tournament, user, request.POST['result'])
                standings = Standing.objects.filter(tournament=tournament)
                if standing_succeed:
                    messages.warning(request, "You successfully added " + str(user))
                else:
                    messages.warning(request, "You already added " + str(user))
                return render(request, 'tournament/report.html',
                              {'tournament': tournament, 'standings': standings, 'report_form': report_form})
            elif request.POST['action'] == "finish":
                if tournament != '0':
                    edited_tournament = finish_tournament(tournament)
                    standings = get_standings_and_leaguepoints(edited_tournament)
                    return render(request, 'tournament/details.html', {'tournament': edited_tournament, 'standings': standings})
        else:
            standings = Standing.objects.filter(tournament=tournament)
            return render(request, 'tournament/report.html',
                          {'tournament': tournament, 'standings': standings, 'report_form': report_form})

    return render(request, 'tournament/report.html', {'tournament': tournament, 'report_form': report_form})


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


def tournament_test(request):
    url = 'http://www.speedrunslive.com/races/result/#!/260116'
    # This does the magic.Loads everything
    r = Render(url)
    # result is a QString.
    result = r.frame.toHtml()

    if request.method == "POST":
        form = NewBracketForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('bracket', tournament_id=post.pk)
    else:
        form = NewBracketForm()

    return render(request, 'tournament/new.html', {'form': form})