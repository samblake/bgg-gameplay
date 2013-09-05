from datetime import date, datetime

class Game():
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.plays = dict()
    
    def __str__(self):
        return '#' + str(self.code) + ' ' + self.name

    def addPlays(self, date, plays):
        month = datetime(date.year, date.month, 1)
        self.plays[month] = plays

    def maxFilteredPlays(self, minMonth):
        filtered = filter(lambda d: d[0] > minMonth, self.plays.iteritems())
        return max(map(lambda x: x[1], filtered))

    def maxPlays(self):
        return max(self.plays.values())

    def totalPlays(self):
        return sum(self.plays.values())
