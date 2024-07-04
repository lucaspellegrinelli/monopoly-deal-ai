import copy
import random
from typing import List

from monopoly.card import Card


# General class for the deck of the cards used in the game.
# In this class, it is also defined the used pile.
class Deck:
    def __init__(self, all_cards: List[Card]):
        self.deck = copy.deepcopy(all_cards)
        self.used_pile: List[Card] = []
        self.shuffle()

    # Shuffles the deck without returning anything
    def shuffle(self):
        random.shuffle(self.deck)

    # Draws the top card of the deck (if any). It is also responsible
    # for shuffling the used pile in the deck if there's no more cards
    # in the deck to be drawn. The card drawn will be returned by this
    # function and removed automatically from the deck. If there's no
    # used pile and no cards left on the deck, an empty array will be
    # returned.
    def draw(self):
        if len(self.deck) == 0 and len(self.used_pile) == 0:
            raise Exception("No more cards to be drawn")

        if len(self.deck) == 0 and len(self.used_pile) > 0:
            self.deck += self.used_pile
            self.used_pile = []
            random.shuffle(self.deck)

        return self.deck.pop(0)

    # Draws 'number' cards from the top of the deck (if there's enough).
    # It uses the function "draw()" to do this, so all the exceptions and
    # added utility implemented in that function also translates to this
    # (like shuffling the used pile into the deck when there's no more
    # cards in it). Cards drawn from this method are automatically removed
    # from the deck.
    def get_cards(self, number: int):
        return [self.draw() for _ in range(number)]

    # Addes the specified card to the used pile
    def add_to_used_pile(self, card):
        self.used_pile.append(card)

    # Creates another object exactly the same as this one
    def copy(self):
        return copy.deepcopy(self)
