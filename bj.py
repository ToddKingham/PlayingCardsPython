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

the_game = Game()

play = True
while play:
    the_game.game_loop()
    play = input('play another round? (y/n): ')[0].lower() == 'y'

print('THANKS FOR PLAYING :)')