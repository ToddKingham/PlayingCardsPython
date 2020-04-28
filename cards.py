from PlayingCards.PlayingCards import PlayingCards

deck = PlayingCards({'jokers':False})
deck.deal(2, 2)

hand = deck.CARDS['hands'][1]

def show():
    for card in hand:
        print(card)


show()

#deck.draw(0)

#show()