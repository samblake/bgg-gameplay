from datetime import date

from game import Game

debug = False

class FlotGen(object):
	def __init__(self, games, maxGames, dateRange):
		self.games = games
		self.maxGames = maxGames
		self.dateRange = dateRange

	def generateData(self):
	    data = []
	    minMonth = max(self.games.itervalues().next().plays) - self.dateRange
	    for game in sorted(self.games.values(), key=lambda g: 1-g.maxFilteredPlays(minMonth)):
	        if debug: print("Adding data for " + game.name)
	        d = []
	        for date in sorted(game.plays): # .iterkeys()?
	            if date > minMonth:
	                d.append([len(d), game.plays[date]])   
	        data.append({'label': game.name, 'data' : d})
	        if len(data) is self.maxGames: break
	    return data

	def generateLabels(self):
	    labels = []
	    i = 0
	    minMonth = max(self.games.itervalues().next().plays) - self.dateRange
	    for date in sorted(self.games.itervalues().next().plays):
	    	if date < minMonth: continue
	        labels.append([str(i), date.strftime('%m-%y')])
	        i += 1
	    return labels