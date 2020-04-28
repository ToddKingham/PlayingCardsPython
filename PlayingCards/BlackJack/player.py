#!/usr/bin/env python

'''Provies a Player class for managing a user state for Blackjack
'''

__author__ = "Todd Kingham"
__copyright__ = "Copyright 2018, Python Learning Project"
__credits__ = ["Todd Kingham"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Todd Kingham"
__email__ = "toddkingham@gmail.com"
__status__ = "Educational"

class Player():
    name= ''
    chips= 0
    
    def __init__(self, name, chips=100):
        self.name = name
        self.chips = chips
        
    def __str__(self):
        return str({
            'name':self.name,
            'chips':self.chips
        })
