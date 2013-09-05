import threading
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from game import Game
from gameScraper import GameScraper
from playsScraper import PlaysScraper

from datetime import datetime

debug = True
bggSite = "http://boardgamegeek.com/"

class BGGScraper(object):
	def __init__(self, maxTries=5):
		self.maxTries = maxTries
		self.now = datetime.now()

	def scrape(self, dateRange, numPages):
		popularGames = self.findPopularGames(numPages)
		self.findPlays(popularGames, dateRange)
		return popularGames

	def findPopularGames(self, numPages):
		popular = {}
		print("Finding popular baord games...")
		for game in GameScraper(bggSite).scrape(numPages):
		    if game is not None and game.code not in popular:
		        popular[game.code] = game
		return popular

	def findPlays(self, popularGames, dateRange):
	    for code in popularGames:
	        game = popularGames[code]
	        print("Scraping plays for " + game.name)
	        self.findTotalPlays(game, dateRange)
	        print(str(game.totalPlays()) + " total plays")

	def findTotalPlays(self, game, delta=relativedelta(years=1)):
	    threads = []
	    for date in self.months(delta):
	        thread = PlaysThread(game, date)
	        threads.append(thread)
	        thread.start()
	    for thread in threads:
	        thread.join()

	def months(self, delta=relativedelta(years=1)):
	    date = self.now - delta
	    month = relativedelta(months=1)
	    while date < self.now:
	        yield date
	        date += month


class PlaysThread(threading.Thread):
    def __init__(self, game, date):
        threading.Thread.__init__(self)
        self.game = game
        self.date = date

    def run(self):
        plays = PlaysScraper(bggSite).scrape(self.game.code, self.date)
        self.game.addPlays(self.date, plays)
        if (debug): print("Total plays for " + self.date.strftime('%m %Y') + ": "+ str(plays))
