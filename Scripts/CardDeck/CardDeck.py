# Program to generate a deck of 52 cards

# Import modules
import itertools
import random


class MyDeck:
    """
    Creates a card deck class with manipulation functions
    Create the deck: 52 / 4 suits = 13 cards per suit
    Where H=Hearts, S=Spades, D=Diamonds, C=Clubs
    """

    def __init__(self):
        self.card_deck = list(itertools.product(['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'], ['H', 'S', 'D', 'C']))

    # Shuffle the deck
    def shuffle_deck(self):
        random.shuffle(self.card_deck)

    # Display the deck
    def print_deck(self):
        print(self.card_deck)


def main():

    a = MyDeck()
    a.shuffle_deck()
    a.print_deck()


if __name__ == '__main__':
    main()
