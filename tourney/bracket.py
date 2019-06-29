import numpy as np


def main():
	br = Bracket()

	entrants = ['Fenyan', 'Malouna', 'Mitsuhito', 'Celthar', 'Souldes', 'Florin', 'Neas', 'Narrow', 'Duanos', 'Aquilion']
	seeds = [5, 3, 2, 7, 1, 8, 9, 4, 6, 10]

	for e, s in zip(entrants, seeds):
		br.add_entrant(Entrant(e, s))
	br.generate_bracket(mode='Distance')
	br.propagate_bracket()

	br.report_bracket()
	# while True:
	# 	a = input('Report match in the format: MatchID,x,y')
	# 	a = a.split(',')
	# 	br.report_match(int(a[0])-1, int(a[1]), int(a[2]))
	for mID in np.arange(15):
		if not br.match_list[mID].played:
			br.report_match(mID, 3, 0)
			br.propagate_bracket()
			br.report_bracket()


class Entrant:
	def __init__(self, pID=None, seed=None):
		self.playerID = pID
		self.seed = seed
		self.isEliminated = False


class Bracket:
	def __init__(self, entrant_list=list(), match_list=list()):
		self.entrant_list = entrant_list
		self.match_list = match_list
		self.bracket_levels = list()
		self.depth = 0
		self.active_round = 0
		self.bracket_finished = False

	def add_entrant(self, entrant):
		self.entrant_list.append(entrant)

	def distance_seeds(self):
		seeds = [1]
		num_entrants = len(self.entrant_list)
		while len(seeds) < num_entrants:
			games = zip(seeds, (2 * len(seeds) + 1 - seed for seed in seeds))
			seeds = [team for game in games for team in game]
		return seeds

	def generate_bracket(self, mode='Distance'):
		self.depth = np.ceil(np.log2(len(self.entrant_list)))
		pl = self.entrant_list
		_, pl = (list(s) for s in zip(*sorted(zip([p.seed for p in pl], pl))))

		seeds, entrants = (list(s) for s in zip(*sorted(zip([p.seed for p in pl], [p.playerID for p in pl]))))

		# round = 0
		round_width = int(2**self.depth)
		while len(pl) < round_width:
			pl.append(Entrant())
		match_counter = 1
		this_levels_matches = list()
		if mode == 'Distance':
			seeds = self.distance_seeds()
		elif mode == 'TopDown':
			seeds = sorted(seeds)
			seeds.extend(np.arange(np.max(seeds)+1, round_width))
		elif mode == 'Entered':
			seeds.extend(np.arange(np.max(seeds)+1, round_width))
		elif mode == 'Random':
			import random
			seeds.extend(np.arange(np.max(seeds)+1, round_width))
			random.shuffle(seeds)

		else:
			print('Mode not found, try again (valid choices: TopDown, Random).')
		for s1, s2 in zip(seeds[::2], seeds[1::2]):
			this_match = Match(match_counter, 0, pl[s1-1], pl[s2-1])
			if (pl[s1-1].playerID is None) or (pl[s2-1].playerID is None):
				this_match.bye_flag = True
				this_match.determine_winner()
			this_match.planned = True
			this_levels_matches.append(this_match)
			self.match_list.append(this_match)
			match_counter += 1

		self.bracket_levels.append(this_levels_matches)

		for level in np.arange(1, self.depth):
			this_levels_matches = list()
			for _ in np.arange(2**(self.depth-level-1)):
				this_match = Match(match_counter, int(level))
				this_levels_matches.append(this_match)
				self.match_list.append(this_match)
				match_counter += 1
			self.bracket_levels.append(this_levels_matches)

	def report_match(self, matchID, score1, score2):
		self.match_list[int(matchID)].set_result((score1, score2))

	def get_childmatch(self, matchID):
		get_match = (matchID+2**self.depth)/2-1
		if np.mod(get_match, 1) > 0:
			get_slot = 0
		else:
			get_slot = 1
		return int(np.ceil(get_match)), get_slot

	def propagate_bracket(self):
		for m in self.bracket_levels[self.active_round]:
			if m.played | m.bye_flag:
				mID, slot = self.get_childmatch(m.matchID)
				if mID > len(self.match_list)-1:
					self.bracket_finished = True
					print('Tournament phase ended!')
					print('Bracket winner: {}'.format(m.winner.playerID))
					break

				if slot == 0:
					self.match_list[mID].p1 = m.winner
				else:
					self.match_list[mID].p2 = m.winner
		if not any([not (c.played | c.bye_flag) for c in self.bracket_levels[self.active_round]]):
			if not self.bracket_finished:
				print('Round {} finished.'.format(self.active_round))
				self.active_round += 1
				self.propagate_bracket()

	def report_bracket(self):
		for i, blvl in enumerate(self.bracket_levels):
			print('Round {}:'.format(i))
			for game in blvl:
				print('Game {} (Round {}: {} ({}) vs. {} ({})'.format(game.matchID, game.depth_level, game.p1.playerID, game.p1.seed,
															game.p2.playerID, game.p2.seed))
				if game.played:
					print('Winner: {}'.format(game.winner.playerID))
			print('')
			print('')
		print('------------------------------')
		print('')
		print('')
		print('')


class Match:
	def __init__(self, matchID, depth_level, p1=Entrant(), p2=Entrant()):
		self.matchID = matchID
		self.depth_level = depth_level
		self.p1 = p1
		self.p2 = p2
		# self.child_match = None
		self.planned = False
		self.played = False
		self.result = (None, None)
		self.winner = None
		self.bye_flag = False

	def set_result(self, result):
		self.result = result
		self.determine_winner()

	def determine_winner(self):
		if not self.bye_flag:
			if self.result[0] > self.result[1]:
				self.winner = self.p1
			elif self.result[1] > self.result[0]:
				self.winner = self.p2
			else:
				self.winner = None
			self.played = True
		else:
			self.winner = self.p1


if __name__ == '__main__':
	main()