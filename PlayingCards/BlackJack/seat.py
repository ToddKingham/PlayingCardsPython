#!/usr/bin/env python

'''Provides a Seat class for storing player and betting states for Blackjack
'''

__author__ = "Todd Kingham"
__copyright__ = "Copyright 2018, Python Learning Project"
__credits__ = ["Todd Kingham"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Todd Kingham"
__email__ = "toddkingham@gmail.com"
__status__ = "Educational"


class Seat():
    player = None
    bets = None

    def __init__(self, player):
        self.player = player
        self.bets = []

    def place_bet(self, bet):
        self.bets.append(bet)

    def clear_bet(self, bet=None):
        if bet is None:
            self.bets = []
        else:
            del self.bets[self.bets.index(bet)]

    def __str__(self):
        return str({
            'player': str(self.player),
            'bets': [','.join([str(bet) for bet in self.bets])]
        })
