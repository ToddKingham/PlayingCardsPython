#!/usr/bin/env python

'''Provides a class to maintain the state of a betting round
'''

__author__ = "Todd Kingham"
__copyright__ = "Copyright 2018, Python Learning Project"
__credits__ = ["Todd Kingham"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Todd Kingham"
__email__ = "toddkingham@gmail.com"
__status__ = "Educational"

class Bet():
    amount= 0
    insurance= 0
    seat= None
    hand= None
    
    def __init__(self, seat, amount=0):
        self.seat = seat
        self.amount = amount
        self.seat.player.chips -= self.amount
    
    def take_insurance(self):
        self.insurance = int(self.amount/2)
        self.seat.player.chips -= self.insurance
    
    def payout_insurance(self):
        self.seat.player.chips += self.insurance*2
        self.insurance = 0

    def set_bet(self, amount):
        self.amount = amount
        self.seat.player.chips -= self.amount

    def double_down(self):
        self.seat.player.chips -= self.amount
        self.amount *= 2

    def surrender_insurance(self):
        self.insurance = 0
    
    def add_hand(self, hand):
        self.hand = hand
    
    def win(self, amount):
        self.seat.player.chips += amount
        self.amount = 0
        
    def loose(self):
        self.amount = 0
    
    def push(self):
        self.win(self.amount)
        
    def __str__(self):
        return str({
            'amount': self.amount,
            'insurance': self.insurance,
            'hand': self.hand
        })
