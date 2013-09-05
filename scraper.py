
from bs4 import BeautifulSoup
import StringIO
import urllib2
import gzip
import itertools

debug = False

def noPagination(page, p):
	return page

class Scraper(object):
	def __init__(self, site, maxTries=5):
	    self.site = site
	    self.maxTries = maxTries

	def decode(self, page):
	    encoding = page.info().get("Content-Encoding")    
	    if encoding in ('gzip', 'x-gzip', 'deflate'):
	        content = page.read()
	        if encoding == 'deflate':
	            data = StringIO.StringIO(zlib.decompress(content))
	        else:
	            data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(content))
	        page = data.read()
	    return page

	def fetch(self, url, count=1):
	    if count > self.maxTries: return None
	    try:
	        return urllib2.urlopen(url)
	    except IOError:
	        return fetch(url, count+1)

	def bSoup(self, url):
	    if (debug): print("Fetching " + url)
	    response = self.decode(self.fetch(url))
	    return BeautifulSoup(response)

	def scrape(self, page, parse, paginate=noPagination, until=None):
		values = []
		url = self.site + page
		for p in itertools.count():
			url = self.site + paginate(page, p+1)
			value = parse(self.bSoup(url))
			values.append(value)
			if until is None or until(value, p+1):
				return values
