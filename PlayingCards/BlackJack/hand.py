#!/usr/bin/env python

'''Provides a Hand state for maintaining the state of a Players cards during a betting round in Blackjack
'''

__author__ = "Todd Kingham"
__copyright__ = "Copyright 2018, Python Learning Project"
__credits__ = ["Todd Kingham"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Todd Kingham"
__email__ = "toddkingham@gmail.com"
__status__ = "Educational"

class Hand:
    cards= []
    bet= 0
    folded= False
    is_blackjack= False

    value= 0
    hidden= False
    soft= False
    can_split= False
    
    
    def __init__(self, cards):
        self.cards = cards
        self.sync()
        self.is_blackjack = self.value == 21
    
    def sync(self):
        indecies = [x.index for x in self.cards]
        self.value = self.calc(self.cards)
        self.hidden = not not list(map(lambda c:c.upcard,self.cards)).count(False)
        self.soft = not not indecies.count('A')
        self.can_split = (lambda a:2 == len(a) == a.count(a[0]))(indecies)
    
    def calc(self, obj):
        values = list(map(self.card_value, obj))
        while sum(values) > 21 and values.count(11):
            values[values.index(11)] = 1
        return sum(values)
    
    def card_value(self, card):
        idx = card.index
        return 11 if idx == 'A' else (10 if not idx.isnumeric() else int(idx))
    
    def fold_hand(self):
        self.folded = True

    def __str__(self):
        return str({
            'cards': [','.join([str(card) for card in self.cards])],
            'value': self.value,
            'soft': self.soft,
            'can_split': self.can_split,
            'bet': self.bet,
            'folded': self.folded,
            'is_blackjack': self.is_blackjack,
            'hidden': self.hidden
        })

         
   