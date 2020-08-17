from pandas import read_csv, Series
import os


def return_goallist():
	pwd = os.getcwd()
	goals_df = read_csv(os.path.join(pwd, 'statistics/goals.csv'))
	total_races = int(goals_df['count'].sum() / 25)
	return list(goals_df.itertuples(index=False, name=None))


def return_playerstats():
	pwd = os.getcwd()
	player_df = read_csv(os.path.join(pwd, 'statistics/players.csv'))
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


def return_race_count():
	pwd = os.getcwd()
	goals_df = read_csv(os.path.join(pwd, 'statistics/goals.csv'))
	total_races = int(goals_df['count'].sum() / 25)
	return total_races