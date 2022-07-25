from pandas import read_csv, Series
import os
import numpy as np


def return_goallist(mode='swiss', year='2021'):
	pwd = os.getcwd()
	if mode == 'swiss':
		goals_df = read_csv(os.path.join(pwd, 'statistics/'+str(year)+'/goals.csv'))
	elif mode == 'top16':
		goals_df = read_csv(os.path.join(pwd, 'statistics/'+str(year)+'/goals_top16.csv'))
	total_races = int(goals_df['count'].sum() / 25)
	return list(goals_df.itertuples(index=False, name=None))


def return_playerstats(mode='swiss', balance='regular', year='2021'):
	pwd = os.getcwd()
	if mode == 'swiss':
		if balance=='regular':
			player_df = read_csv(os.path.join(pwd, 'statistics/'+str(year)+'/players.csv'))
		elif balance=='rebalance':
			player_df = read_csv(os.path.join(pwd, 'statistics/'+str(year)+'/players_rebalanced.csv'))
	elif mode == 'top16':
		if balance == 'regular':
			player_df = read_csv(os.path.join(pwd, 'statistics/'+str(year)+'/players_top16.csv'))
		elif balance == 'rebalance':
			player_df = read_csv(os.path.join(pwd, 'statistics/'+str(year)+'/players_top16_rebalance.csv'))
	return list(player_df.itertuples(index=False, name=None))


def return_goal_combinations(year='2021'):
	pwd = os.getcwd()
	combi_df = read_csv(os.path.join(pwd, 'statistics/'+str(year)+'/combinations.csv'))
	split_fun = lambda r: [s.replace('[', '').replace(']', '').replace('\'', '') for s in r.split('\',')]
	split_fun2 = lambda r: [s for s in r.split('\",')]
	split_combinations = combi_df['goal combination'].apply(split_fun).apply(Series)
	combi_df = combi_df.merge(split_combinations, left_index=True, right_index=True).drop(
		['goal combination'], axis=1)

	return list(combi_df.itertuples(index=False, name=None))


def return_race_count(mode='swiss', year='2021'):
	pwd = os.getcwd()
	if mode == 'swiss':
		goals_df = read_csv(os.path.join(pwd, 'statistics/'+str(year)+'/goals.csv'))
	elif mode == 'top16':
		goals_df = read_csv(os.path.join(pwd, 'statistics/'+str(year)+'/goals_top16.csv'))
	total_races = int(goals_df['count'].sum() / 25)
	return total_races


def return_timestamp(mode, year):
	pwd = os.getcwd()
	if len(mode) > 0:
		timestamp_path = os.path.join(pwd, 'statistics/'+str(year)+'/timestamp_'+mode+'.txt')
	else:
		timestamp_path = os.path.join(pwd, 'statistics/' + str(year) + '/timestamp.txt')
	with open(timestamp_path) as f:
		txt = f.read()
	return txt


def return_first_last_races(version):
	race_first_last = dict()
	if version == 'v10.1':
		race_first_last['first'] = '30.11.2020'
		race_first_last['last'] = '13.07.2022'
	elif version == 'v10.2':
		race_first_last['first'] = '13.07.2022'
		race_first_last['last'] = '-'
	return race_first_last


def return_tournament_url(year):
	if year == '2022':
		return 'https://bingo-tournament.scaramangado.de/'
	else:
		return f"https://xwmtp.github.io/bingo{year}/"
