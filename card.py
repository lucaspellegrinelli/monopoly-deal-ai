import cardconsts
import random

class Card:
  def __init__(self, id, name, value):
    self.id = id
    self.name = name
    self.value = value

class MoneyCard(Card):
  def __init__(self, id, name, value):
    Card.__init__(self, id, name, value)

class ActionCard(Card):
  def __init__(self, id, name, value, action):
    Card.__init__(self, id, name, value)
    self.action = action

class PropertyCard(Card):
  def __init__(self, id, name, value, colors):
    Card.__init__(self, id, name, value)
    self.colors = colors

class RentCard(Card):
  def __init__(self, id, name, value, colors, wild):
    Card.__init__(self, id, name, value)
    self.colors = colors
    self.wild = wild

class Deck:
  def __init__(self):
    self.deck = random.shuffle(list(ALL_CARDS))
    self.used_pile = []

  def draw(self):
    if len(self.deck) == 0:
      self.deck = random.shuffle(list(self.used_pile))
      self.used_pile = []

    return self.deck.pop(0)

  def getCards(self, number):
    cards = []
    for i in range(number):
      cards.append(self.draw())
    return cards
