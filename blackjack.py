#!/usr/bin/env python

''' Blackjack Game simulation based on the PlayingCard and BlackJack classes. Provides the 
    user interface and game flow for a Blackjack Simulation. This file is the game entry point
'''

from PlayingCards.BlackJack.game import Game

__author__ = "Todd Kingham"
__copyright__ = "Copyright 2018, Python Learning Project"
__credits__ = ["Todd Kingham"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Todd Kingham"
__email__ = "toddkingham@gmail.com"
__status__ = "Educational"


def main():
    game = Game()

    play = True
    while play:
        game.game_loop()
        play = input('play another round? (y/n): ')[0].lower() == 'y'

    print('THANKS FOR PLAYING :)')
    print("")

if __name__ == "__main__":
    main()