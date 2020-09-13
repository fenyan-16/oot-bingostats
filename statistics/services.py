from pandas import read_csv, Series
import os
import numpy as np


def return_goallist(mode='swiss'):
	pwd = os.getcwd()
	if mode == 'swiss':
		goals_df = read_csv(os.path.join(pwd, 'statistics/goals.csv'))
	elif mode == 'top16':
		goals_df = read_csv(os.path.join(pwd, 'statistics/goals_top16.csv'))
	total_races = int(goals_df['count'].sum() / 25)
	return list(goals_df.itertuples(index=False, name=None))


def return_playerstats(mode='swiss'):
	pwd = os.getcwd()
	if mode == 'swiss':
		player_df = read_csv(os.path.join(pwd, 'statistics/players.csv'))
	elif mode == 'top16':
		player_df = read_csv(os.path.join(pwd, 'statistics/players_top16.csv'))
	return list(player_df.itertuples(index=False, name=None))


def return_goal_combinations():
	pwd = os.getcwd()
	combi_df = read_csv(os.path.join(pwd, 'statistics/combinations.csv'))
	split_fun = lambda r: [s.replace('[', '').replace(']', '').replace('\'', '') for s in r.split('\',')]
	split_fun2 = lambda r: [s for s in r.split('\",')]
	split_combinations = combi_df['goal combination'].apply(split_fun).apply(Series)
	combi_df = combi_df.merge(split_combinations, left_index=True, right_index=True).drop(
		['Unnamed: 0', 'goal combination'], axis=1)

	return list(combi_df.itertuples(index=False, name=None))


def return_race_count(mode='swiss'):
	pwd = os.getcwd()
	if mode == 'swiss':
		goals_df = read_csv(os.path.join(pwd, 'statistics/goals.csv'))
	elif mode == 'top16':
		goals_df = read_csv(os.path.join(pwd, 'statistics/goals_top16.csv'))
	total_races = int(goals_df['count'].sum() / 25)
	return total_races