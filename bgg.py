#!/usr/bin/env python

import urllib2
import gzip
import pickle
import StringIO
import json
import threading
import itertools
import operator
from bs4 import BeautifulSoup
from string import capwords
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

class Game:
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.plays = dict()
    
    def __str__(self):
        return '#' + str(self.code) + ' ' + self.name

    def addPlays(self, date, plays):
        month = datetime(date.year, date.month, 1)
        self.plays[month] = plays

    def maxFilteredPlays(self, dateRange):
        minMonth = max(popularGames.itervalues().next().plays) - dateRange
        filtered = filter(lambda d: d[0] > minMonth, self.plays.iteritems())
        return max(map(lambda x: x[1], filtered))

    def maxPlays(self):
        return maxPlays(self.plays.values())

    def totalPlays(self):
        return sum(self.plays.values())

def decode(page):
    #if (debug): print(req.info())
    encoding = page.info().get("Content-Encoding")    
    if encoding in ('gzip', 'x-gzip', 'deflate'):
        content = page.read()
        if encoding == 'deflate':
            data = StringIO.StringIO(zlib.decompress(content))
        else:
            data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(content))
        page = data.read()
    return page

def parseGame(soup, divId):
    if (debug): print("Looking for div#" + divId)
    game = soup.find("div", {"id": divId})
    if game is not None:
        link = game.a['href']
        if (debug): print("Found " + link)
        spl = link.split('/')            
        code = int(spl[2])
        name = (' ').join(s.capitalize() for s in spl[3].split('-'))
        print("Found " + name)
        return Game(code, name)
    else:
        if (debug): print("No game found")
    return None

def months(delta=relativedelta(years=1)):
    date = now - delta
    month = relativedelta(months=1)
    while date < now:
        yield date
        date += month

def fetch(url, count=0):
    if count > 5: return None
    try:
        return urllib2.urlopen(url)
    except IOError:
        return fetch(url, count+1)

def bSoup(url):
    if (debug): print("Fetching " + url)
    response = decode(fetch(url))
    return BeautifulSoup(response)

def getPlaysForPage(code, year, month, page):
    url = bggSite + "playstats/thing/" + str(code) + '/' + year + '-' + month + "/page/" + str(page)
    soup = bSoup(url)
    total = 0
    for lf in soup.find_all("td", class_="lf"):
        if 'width' in lf: continue # rank
        total += int(lf.get_text())
    if debug: print("Found " + str(total) + " plays")
    return total

def findPlaysForMonth(code, date):
    year = date.strftime('%Y')
    month = date.strftime('%m')
    totalPlays = 0
    for page in itertools.count():
        plays = getPlaysForPage(code, year, month, page)
        if plays is 0: break
        totalPlays += plays
    return totalPlays

class PlaysThread(threading.Thread):
    def __init__(self, game, date):
        threading.Thread.__init__(self)
        self.game = game
        self.date = date

    def run(self):
        plays = findPlaysForMonth(self.game.code, self.date)
        self.game.addPlays(self.date, plays)
        if (debug): print("Total plays for " + self.date.strftime('%m %Y') + ": "+ str(plays))

def findTotalPlays(game, delta=relativedelta(years=1)):
    threads = []
    for date in months(delta):
        thread = PlaysThread(game, date)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

def findPopularGames():
    print("Finding popular baord games...")
    gameListPage = bggSite + "browse/boardgame/page/"
    for page in xrange(1, numPages+1):
        url = gameListPage + str(page)
        if (debug): print("Fetching " + url)
        soup = bSoup(url)
        for num in xrange(1,100):
            divId = "results_objectname" + str(num)
            game = parseGame(soup, divId)
            if game is not None and game.code not in popularGames:
                popularGames[game.code] = game

def findPlays():
    for code in popularGames:
        game = popularGames[code]
        print("Scraping plays for " + game.name)
        findTotalPlays(game, dateRange)
        print(str(game.totalPlays()) + " total plays")

def scrapeTotalPlays():
    findPopularGames()
    findPlays()
    with open(dataFile, 'a') as f:
        pickle.dump(popularGames, f)

def generateData():
    data = []
    minMonth = max(popularGames.itervalues().next().plays) - dateRange 
    for game in sorted(popularGames.values(), key=lambda g: 1-g.maxFilteredPlays(dateRange)):
        if debug: print("Adding data for " + game.name)
        d = []
        for date in sorted(game.plays): # .iterkeys()?
            if date > minMonth:
                d.append([len(d), game.plays[date]])   
        data.append({'label': game.name, 'data' : d})
        if (len(data) is maxGames): break
    return data

def generateLabels():
    labels = []
    i = 0
    for date in sorted(popularGames.itervalues().next().plays):
        labels.append([str(i), date.strftime('%m-%y')])
        i += 1
    return labels

def generateGraphData():
    print("Generating graph...")
    data = generateData()
    labels = generateLabels()
    with open('json.js', 'wb') as f:
        f.write("var data = " + json.dumps(data, indent=4) + ";\n")
        f.write("var labels = " + json.dumps(labels, indent=4) + ";")


debug = False
popularGames = {}
now = datetime.now()
numPages = 5
maxGames = 25
dateRange = relativedelta(years=5)
bggSite = "http://boardgamegeek.com/"   
dataFile = "stats.data"

try:
    with open(dataFile) as f:
       popularGames = pickle.load(f)
       print("Loaded stats from file")
except IOError:
    scrapeTotalPlays()

generateGraphData()
