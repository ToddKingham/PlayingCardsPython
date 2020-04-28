#!/usr/bin/env python

'''Provides a virtual playing card deck (or decks) specifically designed to retain the physics and properties of a physical deck 
'''

from random import shuffle
from random import randrange
from random import random
from random import randint

__author__ = "Todd Kingham"
__copyright__ = "Copyright 2018, Python Learning Project"
__credits__ = ["Todd Kingham"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Todd Kingham"
__email__ = "toddkingham@gmail.com"
__status__ = "Educational"

class Helpers():
    def plusOrMinus(self, n):
        n = int(n)
        return randint(abs(n)*-1,abs(n)) 
    
    def move(self, src, dest, start=None, count=1, indecies=None, sort=False, reverse=False, face_up=False):
        if indecies is not None:
            indecies.sort()
            indecies.reverse()
            for i in indecies:
                self.move(src, dest, i, 1, face_up=face_up)
        else:         
            if start is None:
                start = 0
                count = len(src)

            cards = self.splice(src, start, count)    

            if sort: cards = cards.sort()
            if reverse: cards = cards.reverse()

            for card in cards:
                card.set_upcard(face_up)
                dest.insert(0,card)
    
    def splice(self, arr, start, count):
        end = start+count
        result = arr[start:end]
        del arr[start:end]
        return result

class Card():
    index= ""
    name= ""
    kind= ""
    suit= ""
    color= ""
    symbol= ""
    upcard= ""
    
    def __init__(self, index, suit, upcard=False):
        deets = self.mappings(index, suit)
        self.index = index
        self.suit = suit
        self.upcard = upcard
        self.name = deets['name']
        self.kind = deets['kind']
        self.color = deets['color']
        self.symbol = deets['symbol']

    def mappings(self, index, suit):
        maps = {
            'A': {'name':'Ace', 'kind':'pip'},
            '2': {'name':'Two', 'kind':'pip'},
            '3': {'name':'Three', 'kind':'pip'},
            '4': {'name':'Four', 'kind':'pip'},
            '5': {'name':'Five', 'kind':'pip'},
            '6': {'name':'Six', 'kind':'pip'},
            '7': {'name':'Seven', 'kind':'pip'},
            '8': {'name':'Eight', 'kind':'pip'},
            '9': {'name':'Nine', 'kind':'pip'},
            '10': {'name':'Ten', 'kind':'pip'},
            'J': {'name':'Jack', 'kind':'face'},
            'Q': {'name':'Queen', 'kind':'face'},
            'K': {'name':'King', 'kind':'face'},
            '%':{'name':'Joker', 'kind':'wild'},
            'Hearts': {'color':'red', 'symbol':'&#9825'},
            'Clubs': {'color':'black', 'symbol':'&#9831'},
            'Diamonds': {'color':'red', 'symbol':'&#9826'},
            'Spades': {'color':'black', 'symbol':'&#9828'},
            'Big': {'color':'black', 'symbol':'&#9787'},
            'Little': {'color':'red', 'symbol':'&#9786'}
        }
        result = maps[index].copy()
        result.update(maps[suit].copy())
        return result
    
    def __str__(self):
        return f"{{ index:{self.index}, name:{self.name}, kind:{self.kind}, suit:{self.suit}, color:{self.color}, symbol:{self.symbol}, upcard:{self.upcard} }}"

    def flip(self):
        self.upcard = not self.upcard
        
    def set_upcard(self, up_or_down):
        self.upcard = up_or_down

class PlayingCards():
    params = {
        "jokers" : True,
        "packs" : 1,
        "discard_up" : False,
        "cards" : [
            {
                "index" : ('A','2','3','4','5','6','7','8','9','10','J','Q','K'),
                "suit" : ('Hearts','Clubs','Diamonds:Desc','Spades:Desc')
            },
            {
                'index':('%'),
                'suit':('Little','Big')
            }
        ]
    }
    
    CARDS = None

    def __init__(self, params=params, deck=None):
        self.CARDS = {
            "stock" : [],
            "discard" : [],
            "table" : [], # maybe we will use this when "laying down" in games such as rummy or even poker games like texas hold 'em
            "hands" : [],
            "dealer" : 0,
            "player" : 1
        }
        
        for key in self.params:
            try:
                self.params[key] = params[key]
            except:
                pass
        
        if deck is None:
            if not self.params['jokers'] and len(self.params['cards']) == 2:
                self.params['cards'].pop()

            for _ in range(self.params['packs']):
                for cardset in self.params['cards']:
                    for s in cardset['suit']:
                        suit = s.split(':')
                        indecies = list(cardset['index'])
                        if len(suit)==2 and suit[1]=='Desc': indecies.reverse()
                        self.CARDS['stock'] += list(map(lambda i: Card(i, suit[0]), indecies))
        else:
            self.CARDS = deck
            
    def shuffle(self, typ=['wash'], pile='stock'):
        def wash(p):
            shuffle(p)
        
        def riffle(p):
            half = int(len(p)/2) 
            for i in range(half):
                p.insert(i+i+randrange(0,3),p.pop(i+half))
           
        def box(p):
            b = []
            quarter = int(len(p)/4)
            for _ in range(3):
                b = Helpers().splice(p,0,quarter+Helpers().plusOrMinus(4)) + b
            p[len(p)::] = b
        
        def cut(p):
            half = int((len(p)/2)+randrange(0,4))
            p[half::] = Helpers().splice(p, 0, half)
        
        def faro(p, out=True):
            x = 1 if out else 0
            half = int(len(p)/2)
            for i in range(half):
                p.insert(i+i+x,p.pop(i+half))

        types = {'wash':wash, 'riffle':riffle, 'box':box, 'cut':cut, 'faro':faro}
        
        for t in typ:
            types[t](self.CARDS[pile])
        
    def deal(self, h=2, n=5, face_up=False):
        result = h*n <= len(self.CARDS['stock'])
        if result:
            d = self.CARDS['dealer']+1
            
            for _ in range(h):
                self.CARDS['hands'].append([])
            
            for i in range(h*n):
                self.draw((i+d)%h, 1, face_up=face_up)
        return result

    def draw(self, idx, count=1, pile='stock', face_up=False):
        if type(pile) is str: 
            pile = self.CARDS[pile]
        Helpers().move(pile, self.CARDS['hands'][idx], 0, count, face_up=face_up)

    def discard(self, h, cards):
        Helpers().move(
            self.CARDS['hands'][h],
            self.CARDS['discard'],
            indecies=cards,
            face_up=self.params['discard_up']
        )
        
    def burn(self, count=1, pile='stock'):        
        Helpers().move(
            self.CARDS[pile],
            self.CARDS['discard'],
            0,
            count,
            face_up=self.params['discard_up']
        )

    def fold(self, idx):
        Helpers().move(self.CARDS['hands'][idx], self.CARDS['discard'])
    
    def flip(self, pile, index=0):
        if pile == 'hands':
            pile = self.CARDS['hands'][index]
        else:
            pile = self.CARDS[pile] 
        pile.reverse()
        list(map(lambda card:card.flip(), pile))
    
    def give(self, src_idx, dest_idx, cards, face_up=False):
        Helpers().move(
            self.CARDS['hands'][src_idx],
            self.CARDS['hands'][dest_idx],
            indecies=cards,
            face_up=face_up
        )
    
    def pickup(self, idx, count=1):
        Helpers().move(
            self.CARDS['discard'],
            self.CARDS['hands'][idx],
            0,
            count
        )
    
    def restock(self, shuf=[]):
        Helpers().move(self.CARDS['discard'], self.CARDS['stock'])
        if len(shuf):
            self.shuffle(shuf)

    def end(self, shuf=[], restock=True):
        for i in range(len(self.CARDS['hands'])):
            Helpers().move(
                self.CARDS['hands'].pop(), 
                self.CARDS['discard']
            )
        Helpers().move(self.CARDS['table'], self.CARDS['discard'])
        
        if restock:
            self.restock(shuf)

