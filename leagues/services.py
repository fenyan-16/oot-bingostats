from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, ListView
from .models import TournamentsInLeague, User, League, Ratingpoints
from tournament.models import Tournament, Standing
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
import datetime
import pandas as pd


def create_league(
		owner: User,
		name: str,
		description: str,
		start_date: datetime,
		end_date: datetime,
) -> League:
	league = League(owner=owner, name=name, description=description, start_date=start_date, end_date=end_date)
	league.save()

	return (league)


def create_ranting_points(
		league: League,
		tournament: Tournament,
		user: User,
		points: int
) -> Ratingpoints:
	rating = Ratingpoints(league=league, tournament=tournament, user=user, points=points)
	rating.save()


def add_tournament_in_league(
		tournament: Tournament,
		league: League,
) -> TournamentsInLeague:
	tournamentInLeague = TournamentsInLeague(tournament=tournament, league=league)
	tournamentInLeague.save()


def get_tournaments_in_league(league_id: int):
	standings_per_tournament = list()
	leaguepoints_per_tournament = list()
	league = League.objects.get(pk=league_id)
	# all Tournaments that belong this league
	# ToDo: Order by Tournament.date
	tournaments_per_league = TournamentsInLeague.objects.filter(league=league).order_by('-tournament')
	for tournament in tournaments_per_league:
		standings = Standing.objects.filter(tournament=tournament.tournament).order_by('placement')
		standings_per_tournament.append(standings)

		leaguepoints_list = list()
		for standing in standings:
			try:
				leagueinformation = Ratingpoints.objects.get(user=standing.user, tournament=standing.tournament)
				leaguepoints_list.append(leagueinformation.points)
			except ObjectDoesNotExist:
				leaguepoints_list.append(None)
		leaguepoints_per_tournament.append(leaguepoints_list)
	return (standings_per_tournament, leaguepoints_per_tournament)


def get_average_times(league_id: int, ratings_and_users):
	league = League.objects.get(pk=league_id)
	tournaments_in_leagues = TournamentsInLeague.objects.filter(league=league)

	standings_in_league = list()
	for t in tournaments_in_leagues:
		for s in Standing.objects.filter(tournament=t.tournament):
			standings_in_league.append((s.user, s.result))

	# standings_in_league = Tournament.objects.filter(tournament=)

	user_results = dict()
	for user in ratings_and_users:
		user_results[user.username] = list()

	for standing in standings_in_league:
		user_results[standing[0].username].append(pd.to_timedelta(standing[1]))

		# users_df = pd.DataFrame(user_results)

	# for user, result_list in user_results.items():
	# 	t_series = pd.Series([pd.to_timedelta(d) for d in result_list)

	tds = [pd.to_timedelta(d).to_series().mean().components for _, d in user_results.items()]
	avg_list = ["{:02d}".format(t.hours)+':'+"{:02d}".format(t.minutes)+':'+"{:02d}".format(t.seconds) for t in tds]

	return avg_list
	# for key, value in user_results.items():


def get_rating_table(league_id: int):
	ratings_list = list()
	users_list = list()
	participation_list = list()
	league = League.objects.get(pk=league_id)

	try:
		ratings = Ratingpoints.objects.filter(league=league).order_by("user")

		this_user = ratings.first().user
		user_points = 0
		participation_counter = 0
		for rating in ratings:
			if this_user == rating.user:
				user_points += rating.points
				participation_counter += 1
			else:
				users_list.append(this_user)
				ratings_list.append(user_points)
				participation_list.append(participation_counter)
				this_user = rating.user
				user_points = rating.points
				participation_counter = 1
		users_list.append(this_user)
		ratings_list.append(user_points)
		participation_list.append(participation_counter)
	except ObjectDoesNotExist:
		print("no Rating points available")

	avg_list = get_average_times(league_id, users_list)

	# indexes = list(range(len(users_list))).sort(key=ratings_list.__getitem__)
	# users_zip_ratingpoints = zip(list(map(users_list.__getitem__, indexes)), list(map(ratings_list.__getitem__, indexes)))
	users_zip_ratingpoints = list(
		reversed(sorted(zip(ratings_list, users_list, participation_list, avg_list), key=lambda x: x[0])))
	return (users_zip_ratingpoints)


def delete_tournament_from_league(league: League, tournament_id: int):
	tournament = Tournament.objects.get(pk=tournament_id)
	TournamentsInLeague.objects.get(league=league, tournament=tournament).exists().delete()
	Ratingpoints.objects.filter(league=league, tournament=tournament).exists().delete()
