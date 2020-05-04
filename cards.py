from PlayingCards.playing_cards import PlayingCards








def main():

    decks = input("How many decks would you like to use? ")
    jokers = True if input("Include Jokers? (y/n) ")[0].lower() === 'y' else False"["

    print("Thank you! We will now build your deck.")
    hands = input("How many hands would you like to deal? ")
    cards = input("And finally... How many cards per hand? ")

    deck = PlayingCards({'jokers': False})
    deck.deal(, 2)



    for card in hand:
        print(card)

#deck.draw(0)

#show()


if __name__ == "__main__":
    main()