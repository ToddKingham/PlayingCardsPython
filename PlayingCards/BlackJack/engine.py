#!/usr/bin/env python

'''
    Provides a BlackJack class. This module provides methods
    to manage all game mechanics of a Blackjack game
'''

from ..playing_cards import PlayingCards
from itertools import chain

from .seat import Seat
from .player import Player
from .bet import Bet
from .hand import Hand

__author__ = "Todd Kingham"
__copyright__ = "Copyright 2018, Python Learning Project"
__credits__ = ["Todd Kingham"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Todd Kingham"
__email__ = "toddkingham@gmail.com"
__status__ = "Educational"


class BlackJackEngine(PlayingCards):
    seats= []
    bets= []
    min_bet= 0
    max_bet= 0
    bank= 0
    shoe= 0
    state= "ready"
    dealer_stands_on= 0
    blackjack_pays= 1
    test = 0
    house_name= "House"
    offer_insurance= False

    
    def __init__(self, seats=7, min_bet=20, max_bet=1000, bank=1000000000, shoe=6, dealer_stands_on=17, blackjack_pays="3:2"):
        self.seats = [None]*(7+1)
        self.bets = []
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.bank = bank
        self.shoe = shoe
        self.dealer_stands_on = dealer_stands_on
        
        bjp = list(map(int,blackjack_pays.split(':')))
        self.blackjack_pays = bjp[0]/bjp[1]
        
        PlayingCards.__init__(self, {'packs':self.shoe, 'jokers':False})
        PlayingCards.end(self)
        self.add_player(Player(self.house_name, self.bank), 0)

    def get_free_seats(self):
        _map = lambda s:s[0] if s[1]==None else None
        _filter = lambda i:i!=None
        return list(filter(_filter, map(_map, enumerate(self.seats))))

    def add_player(self, player, seat):
        if not self.seats[seat]:
            self.seats[seat] = Seat(player)
        
    def remove_player(self, seat):
        self.seats[seat] = None

    def place_bet(self, seat, amount):
        result = str(amount).isnumeric()
        if result:
            amount = int(amount)
            if self.min_bet <= amount <= min(seat.player.chips, self.max_bet):
                bet = Bet(seat, amount)
                seat.place_bet(bet)
                self.bets.append(bet)
            elif amount:
                return False

        return result

    def begin(self):
        if self.state == 'ready' and len(self.bets):
                
            self.state = 'playing'

            #add dealers bet
            dealer_bet = Bet(self.seats[0],0)
            self.bets = [dealer_bet] + self.bets.copy()
            self.seats[0].place_bet(dealer_bet)
            
            #deal initial cards
            self.deal()
            
            #calculate if insurance is needed
            dealers_hand = self.get_dealers_hand()
            upcard = dealers_hand.cards[1]
            self.offer_insurance = dealers_hand.card_value(upcard) >= 10

    def dealer_blackjack_check(self):                
        result = self.get_dealers_hand().is_blackjack

        def settle_bets(bet):
                if bet.insurance:
                    bet.payout_insurance()

                if bet.hand.is_blackjack:
                    bet.push()
                else:
                    bet.loose()

        if result:
            self.CARDS['hands'][0][0].flip()
            map(settle_bets, self.bets)
        else:
            map(lambda b:b.surrender_insurance(), self.bets)

        return result

    def valid_actions(self, bet):
            actions = ['hit','stand']
            has_aces = list(map(lambda c:c.index, bet.hand.cards)).count('A')
            has_split = len(bet.seat.bets) > 1
        
            if bet.hand.can_split:
                actions.append('split')
            if len(bet.hand.cards) and (not (has_aces and has_split)):
                actions.append('double')
            if (not has_split) and (len(bet.hand.cards)==2):
                actions.append('surrender')
            return set(actions)

    def do_action(self, bet, action):
        result = True
        action = action.lower()
        
        if not {action}.issubset(self.valid_actions(bet)):
            return result
        
        ### HIT
        if action == 'hit':
            self.hit(bet.hand)
            if bet.hand.value > 21:
                bet.hand.fold_hand()
                bet.loose()
                result = False


        ### DOUBLE DOWN
        elif action == 'double':
            self.hit(bet.hand)
            bet.double_down()
            if bet.hand.value > 21:
                bet.hand.fold_hand()
                bet.loose()
            result = False


        ### SPLIT
        elif action == 'split':
            #deal a new empty hand into the game.
            new_bet = Bet(bet.seat, bet.amount)
            self.bets.insert(self.bets.index(bet)+1, new_bet )
            bet.seat.place_bet(new_bet)
            self.deal(cards=0)

            #move 1 card from the original hand into the new hand just created
            src_idx = self.CARDS['hands'].index(bet.hand.cards)
            dest_idx = len(self.CARDS['hands'])-1
            self.give(src_idx, dest_idx, [1], face_up=True)

            #draw a new card into the original hand
            self.hit(bet.hand)


        ### SURRENDER
        elif action == 'surrender':
            bet.hand.fold_hand()
            bet.win(bet.amount/2)
            result = False
            

        ### STAND
        elif action == 'stand':
            result = False


        return result
    
    ##### GETTERS #####
    def get_dealer(self):
        return self.seats[0]

    def get_dealers_hand(self):
        return self.get_dealer().bets[0].hand

    def get_dealers_upcard(self):
        return list(filter(lambda c:c.upcard , self.get_dealers_hand().cards))[0]

    def get_seats(self):
        return list(filter(lambda s:s!=None and s.player.name!=self.house_name, [seat for seat in self.seats]))

    def get_bets(self):
        return list(filter(lambda b:b.seat.player.name != self.house_name, self.bets))
    
    def get_open_bets(self):
        return list(filter(lambda b:not b.hand.folded, self.get_bets()))

    #=================================#
    def deal(self, cards=2 ):
        unfilled_bets = list(filter(lambda b:b.hand==None, self.bets))
        PlayingCards.deal(self, len(unfilled_bets), cards, face_up=True)
        hands = self.CARDS['hands']
        
        for i, bet in enumerate(unfilled_bets):
            if bet.seat.player.name == self.house_name:
                self.CARDS['hands'][0][0].flip()
            bet.add_hand(Hand(hands[(len(hands)-len(unfilled_bets))+i]))

    def hit(self, hand):
        PlayingCards.draw(self, self.CARDS['hands'].index(hand.cards), 1, face_up=True)
        hand.sync()
    
    def end(self):
        #discard all cards in play
        PlayingCards.end(self, restock=False)
        
        #remove all bets
        for seat in self.seats:
            if seat:
                seat.clear_bet()
        self.bets = []

        #reset table    
        self.state = 'ready'
