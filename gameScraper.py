from scraper import Scraper
from game import Game
import operator

debug = False
url = "browse/boardgame/page/"

class GameScraper(object):
	def __init__(self, site, maxTries=5):
		self.scraper = Scraper(site, maxTries)

	def scrape(self, maxPages):
		until = lambda v, p: p == maxPages
		gamesList = self.scraper.scrape(url, self.parse, self.paginate, until)
		return reduce(operator.add, gamesList)
		
	def parse(self, soup):
		games = []
		for num in xrange(1,100):
		    divId = "results_objectname" + str(num)
		    games.append(self.parseGame(soup, divId))
		return games

	def parseGame(self, soup, divId):
		if (debug): print("Looking for div#" + divId)
		game = soup.find("div", {"id": divId})
		link = game.a['href']
		if (debug): print("Found " + link)
		spl = link.split('/')
		code = int(spl[2])
		name = (' ').join(s.capitalize() for s in spl[3].split('-'))
		print("Found " + name)
		return Game(code, name)

	def paginate(self, url, p):
		return url + str(p) + "/"
