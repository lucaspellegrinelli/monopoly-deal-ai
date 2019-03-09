import copy
import random

class Deck:
  def __init__(self, all_cards):
    self.deck = copy.deepcopy(all_cards)
    self.shuffle()
    self.used_pile = []

  def shuffle(self):
    random.shuffle(self.deck)

  def draw(self):
    if len(self.deck) == 0 and len(self.used_pile) > 0:
      self.deck = copy.deepcopy(self.used_pile)
      random.shuffle(self.deck)
      self.used_pile = []
    elif len(self.deck) == 0 and len(self.used_pile) == 0:
      return []

    return self.deck.pop(0)

  def getCards(self, number):
    cards = []
    for i in range(number):
      if len(self.deck) == 0 and len(self.used_pile) == 0:
        break
      cards.append(self.draw())

    return cards

  def addToUsedPile(self, card):
    self.used_pile.append(card)
