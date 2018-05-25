#!/usr/bin/env python

''' Blackjack Game simulation based on the PlayingCard and BlackJack classes. Provides the 
    user interface and game flow for a Blackjack Simulation. This file is the game entry point
'''

from blackjack import Game

__author__ = "Todd Kingham"
__copyright__ = "Copyright 2018, Python Learning Project"
__credits__ = ["Todd Kingham"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Todd Kingham"
__email__ = "toddkingham@gmail.com"
__status__ = "Educational"


class Strategy():
    matrix = None
    action_map = {
        'H':'hit',
        'S':'stand',
        'D':'double',
        'P':'split',
        'X':'surrender',
    }

    def __init__(self, strategy='advanced'):
        self.matrix = self.get_strategy(strategy)


    def action(self, hand, d_hand):
        if hand.value == 21:
            return 'stand'
        return self.action_map.get(self.matrix[self.hand_value(hand)][self.dealers_upcard(d_hand)])

    def hand_value(self, hand):
        if hand.can_split:
            val = hand.card_value(hand.cards[0])
            return 'pair_' + ('A' if val == 11 else str(val))
        elif hand.soft and hand.value > 12:
            return 'soft_' + str(hand.value)
        else:
            return str(hand.value)

    def dealers_upcard(self, hand):
        return hand.card_value(list(filter(lambda c:c.upcard , hand.cards))[0])-2
        #return 

    def get_strategy(self, key):
        stragegies = {
            'advanced': {
                '5':        ['H','H','H','H','H','H','H','H','H','H'],
                '6':        ['H','H','H','H','H','H','H','H','H','H'],
                '7':        ['H','H','H','H','H','H','H','H','H','H'],
                '8':        ['H','H','H','H','H','H','H','H','H','H'],
                '9':        ['H','D','D','D','D','H','H','H','H','H'],
                '10':       ['D','D','D','D','D','D','D','D','H','H'],
                '11':       ['D','D','D','D','D','D','D','D','D','H'],
                '12':       ['H','H','S','S','S','H','H','H','H','H'],
                '13':       ['S','S','S','S','S','H','H','H','H','H'],
                '14':       ['S','S','S','S','S','H','H','H','H','H'],
                '15':       ['S','S','S','S','S','H','H','H','X','X'],
                '16':       ['S','S','S','S','S','H','H','X','X','X'],
                '17':       ['S','S','S','S','S','S','S','S','S','X'],
                '18':       ['S','S','S','S','S','S','S','S','S','S'],
                '19':       ['S','S','S','S','S','S','S','S','S','S'],
                '20':       ['S','S','S','S','S','S','S','S','S','S'],
                
                'soft_13':  ['H','H','H','D','D','H','H','H','H','H'],
                'soft_14':  ['H','H','H','D','D','H','H','H','H','H'],
                'soft_15':  ['H','H','D','D','D','H','H','H','H','H'],
                'soft_16':  ['H','H','D','D','D','H','H','H','H','H'],
                'soft_17':  ['H','D','D','D','D','H','H','H','H','H'],
                'soft_18':  ['S','D','D','D','D','S','S','H','H','H'],
                'soft_19':  ['S','S','S','S','S','S','S','S','S','S'],
                'soft_20':  ['S','S','S','S','S','S','S','S','S','S'],
                
                'pair_A':   ['P','P','P','P','P','P','P','P','P','P'],
                'pair_2':   ['P','P','P','P','P','P','H','H','H','H'],
                'pair_3':   ['P','P','P','P','P','P','H','H','H','H'],
                'pair_4':   ['H','H','H','P','P','H','H','H','H','H'],
                'pair_5':   ['D','D','D','D','D','D','D','D','H','H'],
                'pair_6':   ['P','P','P','P','P','H','H','H','H','H'],
                'pair_7':   ['P','P','P','P','P','P','H','H','H','H'],
                'pair_8':   ['P','P','P','P','P','P','P','P','P','P'],
                'pair_9':   ['P','P','P','P','P','S','P','P','S','S'],
                'pair_10':  ['S','S','S','S','S','S','S','S','S','S']
            }
        }
        return stragegies[key]

# table = BlackJack()

# seat = itter(table.get_free_seats())


class AutoGame(Game):

    strategy = None

    def __init__(self, strategy="advanced"):
        self.strategy = Strategy(strategy)
        Game.__init__(self)

    def bet_input(self, msg):
        return 20

    def insurance_input(self, msg):
        print('hi')
        return 'n'

    def action_input(self, bet, actions):
        return self.strategy.action(bet.hand, self.table.get_dealers_hand())

game = AutoGame()
for _ in range(2):
    game.game_loop()
