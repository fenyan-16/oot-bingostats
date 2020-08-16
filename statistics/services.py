from pandas import read_csv
import os


def return_goallist():
	pwd = os.getcwd()
	goals_df = read_csv(os.path.join(pwd, 'statistics/goals.csv'))
	return list(goals_df.itertuples(index=False, name=None))


def return_playerstats():
	player_df = read_csv('statistics/players.csv')
	return list(player_df.itertuples(index=False, name=None))
