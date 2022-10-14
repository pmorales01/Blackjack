# Pedro Morales
# CPSC 386-03
# 2022-03-16
# pedrom2@csu.fullerton.edu
# @pedromorales451
#
# Lab 03-00
#
# This file contains and defines the Deck and Card classes.
#

"""A French suited playing card class and a Deck of 52 cards class."""

from collections import namedtuple
from random import shuffle, randrange

Card = namedtuple("Card", ["rank", "suit"])


def _str_card(card):
    """Convert card to string."""
    return f"{card.rank} of {card.suit}"


# redefine Card's __str__ to _str_card()
Card.__str__ = _str_card


class Deck:
    """Deck class to hold 52 playing cards."""

    ranks = ["Ace"] + [str(x) for x in range(2, 11)] + "Jack Queen King".split()
    suits = "Clubs Hearts Spades Diamonds".split()
    values = list(range(1, 11)) + [10, 10, 10]
    value_dict = dict(zip(ranks, values))

    def __init__(self):
        """Create a deck of cards."""
        self._cards = [
            Card(rank, suit) for suit in self.suits for rank in self.ranks
        ]

    def __len__(self):
        """Return the number of cards in the deck."""
        return len(self._cards)

    def __getitem__(self, position):
        """Return the card at the given position."""
        return self._cards[position]

    def shuffle(self, n_shuffles=1):
        """Shuffle the deck n times. Default is 1 time."""
        for _ in range(n_shuffles):
            shuffle(self._cards)

    def cut(self):
        """Splits the deck and places a cut card between 60th and 80th card."""
        half = 70 + randrange(-9, 10)
        bottomhalf = self._cards[:half]
        tophalf = self._cards[half:]
        self._cards = bottomhalf + ["CUT CARD"] + tophalf

    def deal(self, n_cards=1):
        """Deal n cards. Default is 1 card."""
        return [self._cards.pop() for x in range(n_cards)]

    def merge(self, other_deck):
        """Merge the current deck with the deck passed as a parameter."""
        self._cards = self._cards + other_deck.deal(len(other_deck))

    def __str__(self):
        """Convert the deck to a string."""
        return ", ".join(map(str, self._cards))


@property
def card_value(card):
    """Return the numerical value of the rank of a given card."""
    return Deck.value_dict[card.rank]


# Methods to lookup a card's value or convert to an integer value
Card.value = card_value
Card.__int__ = card_value
