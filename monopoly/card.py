import copy
import random

# Property Card Flags
GREEN_PROPERTY = 0
DARK_BLUE_PROPERTY = 1
LIGHT_BLUE_PROPERTY = 2
RED_PROPERTY = 3
LIGHT_GREEN_PROPERTY = 4
YELLOW_PROPERTY = 5
ORANGE_PROPERTY = 6
BROWN_PROPERTY = 7
PINK_PROPERTY = 8
BLACK_PROPERTY = 9
RAINBOW_PROPERTY = 10

class Card:
  def __init__(self, id, name, value):
    self.id = id
    self.name = name
    self.value = value

  def __eq__(self, other):
    return type(self) == type(other) and self.id == other.id

  def __ne__(self, other):
    return not self.__eq__(other)

  def __repr__(self):
    return self.name

class MoneyCard(Card):
  def __init__(self, id, name, value):
    Card.__init__(self, id, name, value)

  def __eq__(self, other):
    Card.__eq__(self, other)

  def __ne__(self, other):
    Card.__ne__(self, other)

class ActionCard(Card):
  def __init__(self, id, name, value, action):
    Card.__init__(self, id, name, value)
    self.action = action

  def __eq__(self, other):
    Card.__eq__(self, other)

  def __ne__(self, other):
    Card.__ne__(self, other)

class PropertyCard(Card):
  def __init__(self, id, name, value, colors):
    Card.__init__(self, id, name, value)
    self.colors = colors

  def isRainbow(self):
    return self.colors[0] == 10

  def __eq__(self, other):
    Card.__eq__(self, other)

  def __ne__(self, other):
    Card.__ne__(self, other)

class RentCard(Card):
  def __init__(self, id, name, value, colors, wild):
    Card.__init__(self, id, name, value)
    self.colors = colors
    self.wild = wild

  def __eq__(self, other):
    Card.__eq__(self, other)

  def __ne__(self, other):
    Card.__ne__(self, other)