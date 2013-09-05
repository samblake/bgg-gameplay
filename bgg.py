#!/usr/bin/env python

import json
import pickle
from dateutil.relativedelta import relativedelta
from flotGen import FlotGen
from bggScraper import BGGScraper
from game import Game

def scrapeGameDate(dateRange, numPages):
    gameData = BGGScraper("http://boardgamegeek.com/").scrape(dateRange, numPages)
    with open(dataFile, 'a') as f:
        pickle.dump(gameData, f)
    return gameData

def generateGraphData(gameData):
    print("Generating graph...")
    flotHelper = FlotGen(gameData, maxGames, dateRange)
    data = flotHelper.generateData()
    labels = flotHelper.generateLabels()
    with open('json.js', 'wb') as f:
        f.write("var data = " + json.dumps(data, indent=4) + ";\n")
        f.write("var labels = " + json.dumps(labels, indent=4) + ";")

maxGames = 50
dateRange = relativedelta(years=1)
dataFile = "stats.data"
numPages = 1

gameData = {}
try:
    with open(dataFile) as f:
       gameData = pickle.load(f)
       print("Loaded stats from file")
except IOError:
    gameData = scrapeGameDate(dateRange, numPages)

generateGraphData(gameData)
