#!/usr/bin/env python

''' Blackjack Game simulation based on the PlayingCard and BlackJack classes. Provides the 
    user interface and game flow for a Blackjack Simulation. This file is the game entry point
'''

import os
from time import sleep

from PlayingCards.BlackJack.BlackJack import BlackJack
from PlayingCards.BlackJack.Player import Player

__author__ = "Todd Kingham"
__copyright__ = "Copyright 2018, Python Learning Project"
__credits__ = ["Todd Kingham"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Todd Kingham"
__email__ = "toddkingham@gmail.com"
__status__ = "Educational"


class Game():
    table= None
    restock_count= 50
    shuffle_list= ['riffle','riffle','box','riffle','cut']
    action_map = {
        'H':'hit',
        'S':'stand',
        'D':'double',
        'P':'split',
        'X':'surrender',
    }

    def __init__(self):
        self.table = BlackJack()
        #self.table.get_free_seats() #<=== get an array of free seat indecies to use in .add_player()
        self.table.add_player(Player('Player 1',1000),1)
        # self.table.add_player(Player('Player 2',1000),2)
        # self.table.add_player(Player('Player 3',1000),3)
        # self.table.add_player(Player('Player 4',1000),4)
        self.table.shuffle(['wash']+self.shuffle_list)
        #self.table.burn(24)

    def display(self, current_bet=None, msg=None):
        os.system('clear')
        def hand_value(hand):
            if [card.upcard for card in hand.cards].count(False):
                return '?'
            elif hand.is_blackjack:
                return 'BLACKJACK!'
            elif hand.value > 21:
                return 'BUST'
            else:
                return str(hand.value)

        def record(seat, show_chips=True):
            player_str = f"{seat.player.name}:"
            if show_chips:
                player_str += f" chips={str(seat.player.chips)}"
            print(player_str)
            for bet in seat.bets:
                card_str = f"{'>' if bet == current_bet else ' '} "
                for card in bet.hand.cards:
                    card_str += f"[{card.index if card.upcard else ' '}] "
                card_str += f"= {hand_value(bet.hand)}"
                print(card_str)
                print('')
            if not len(seat.bets):
                print(' ')
        
        print('----------------------------------------------------')
        record(self.table.get_dealer(),False)
        for seat in self.table.get_seats():
            record(seat) 
        print('----------------------------------------------------')
        if msg:
            print(msg)

    def place_bets(self):
        for seat in self.table.get_seats():
            bet_placed = False
            while not bet_placed:
                bet_placed = self.table.place_bet(
                    seat,
                    self.bet_input(f"{seat.player.name}: Enter a bet between {str(self.table.min_bet)} and {str(min(seat.player.chips,self.table.max_bet))} (enter 0 to pass) ")
                )

    def deal_cards(self):
        self.table.begin()
        self.display()

    def insurance_check(self):
        if self.table.offer_insurance:
            for bet in self.table.get_bets():
                if self.insurance_input(bet):
                    bet.take_insurance()
            self.display()
    
    def dealer_blackjack_check(self):
        dealers_hand = self.table.get_dealers_hand()
        if dealers_hand.is_blackjack:
            dealers_hand.cards[0].flip()
            for bet in self.table.get_bets():
                #payout insurance
                if bet.insurance:
                    bet.payout_insurance()
                #surrender bets
                if bet.hand.is_blackjack:
                    bet.push()
                else:
                    bet.loose()
            self.display()
            print('dealer wins')
            self.table.end()
            return True
        else:
            return False

    def colllect_insurance_bets(self):
        if self.table.offer_insurance:
            print('COLLECT INS!')
            for bet in self.table.get_bets():
                if bet.insurance:
                    bet.surrender_insurance()

    def payout_blackacks(self):
        naturals = list(filter(lambda b:b.hand.is_blackjack, self.table.get_bets()))
        for bet in naturals:
            bet.hand.fold_hand()
            bet.win(bet.amount + (bet.amount*self.table.blackjack_pays))
        if len(naturals):
            self.display()

    def betting_loop(self):
        for bet in self.table.bets:
            if bet.seat.player.name != self.table.house_name and not bet.hand.folded:

                self.display(bet)
                #STEP 1: In case of a previous "split" this hand COULD have only 1 card, so let's fix that
                if len(bet.hand.cards) == 1:
                    self.table.hit(bet.hand)
                    self.display(bet)

                #STEP 2: Now let's run the main loop to see what action the player wants to take on this hand
                cont = True
                while cont:
                    #get allowed actions based on the current 
                    authorized_actions = self.table.valid_actions(bet)

                    #let the player enter their desired action
                    action = self.action_input(bet, authorized_actions)

                    #validate the action is supported then process the action
                    if {action}.issubset(authorized_actions):
                        cont = self.table.do_action(bet, action)
                        self.display(bet)

    def dealer_action(self):
        dealers_hand = self.table.get_dealers_hand()
        dealers_hand.cards[0].flip()
        self.display()
        sleep(1)

        if len(self.table.get_open_bets()):
            while True:
                dealers_hand = self.table.get_dealers_hand()
                if dealers_hand.value < self.table.dealer_stands_on:
                    self.table.hit(dealers_hand)
                    self.display()
                    sleep(1)
                else:
                    break
        return dealers_hand

    def bust_dealer(self):
        messages=[]
        for bet in self.table.get_open_bets():
            bet.win(bet.amount*2)
            messages.append(f"{bet.seat.player.name}: You win!")
        self.display()
        for msg in messages:
            print(msg)    
        self.table.end()

    def payout_bets(self, dealers_hand):
        messages=[]
        for bet in self.table.get_open_bets():
            if bet.hand.value > dealers_hand.value:
                bet.win(bet.amount*2)
                messages.append(f"{bet.seat.player.name}: You win!")
            elif bet.hand.value < dealers_hand.value:
                bet.loose()
                messages.append(f"{bet.seat.player.name}: You loose!")
            else:
                bet.push()
                messages.append(f"{bet.seat.player.name}: Pushed!")
        self.display()
        for msg in messages:
            print(msg)
        self.table.end()

    def shuffle(self):
        self.table.restock(self.shuffle_list)

    def bet_input(self, msg):
        return input(msg)
    
    def insurance_input(self, bet):
            input(f"{bet.seat.player.name}: would you like insurance? (y/n): ")[0].lower() == 'y'

    def action_input(self, bet, actions):
        def msg(act):
            msg = f"{bet.seat.player.name}: Hit(h) | Stand(s) "
            if {'split'}.issubset(act):
                msg += '| Split(p) '
            if {'double'}.issubset(act):
                msg += '| Double Down(d) '
            if {'surrender'}.issubset(act):
                msg += '| Surrender(x) '
            return msg

        return self.action_map.get(input(msg(actions))[0].upper())

    def game_loop(self):
        os.system('clear')

        if len(self.table.CARDS['stock']) <= self.restock_count:
            self.shuffle()
        print()

        #place bets
        self.place_bets()

        #deal cards
        self.deal_cards()

        #ask for insurance: if applicable
        self.insurance_check()        

        #if dealer has a natural
        if self.dealer_blackjack_check():
            return

        #collect insurance bets
        self.colllect_insurance_bets()

        #pay out all naturals
        self.payout_blackacks()

        #LOOP bets:
        self.betting_loop()
    
        #LOOP dealer action (hit until 17):
        dealers_hand = self.dealer_action()

        #if dealer busts
        if dealers_hand.value > 21:
            self.bust_dealer()
            return

        #LOOP remaining bets
        self.payout_bets(dealers_hand)

        return
