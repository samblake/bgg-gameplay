from scraper import Scraper

debug = True

class PlaysScraper(object):
	def __init__(self, site, maxTries=5):
		self.scraper = Scraper(site, maxTries)

	def scrape(self, code, date):
		year = date.strftime('%Y')
		month = date.strftime('%m')
		url = "playstats/thing/" + str(code) + '/' + year + '-' + month + "/page/"
		return sum(self.scraper.scrape(url, self.parse, self.paginate, self.until))

	def parse(self, soup):
		total = 0
		for lf in soup.find_all("td", class_="lf"):
			if 'width' in lf: continue # ranking
			total += int(lf.get_text())
		return total

	def paginate(self, url, p):
		return url + str(p)

	def until(self, value, p):
		return value == 0

