from cardconsts import *
import copy
import random

class Card:
  def __init__(self, id, name, value):
    self.id = id
    self.name = name
    self.value = value

  def __repr__(self):
    return self.name

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
  def __init__(self, all_cards):
    self.deck = copy.deepcopy(all_cards)
    random.shuffle(self.deck)
    self.used_pile = []

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
      cards.append(self.draw())
    return cards

class PropertySet:
  def __init__(self, colors):
    self.properties = []
    self.colors = colors
    self.hasHouse = False
    self.hasHotel = False

  def addProperty(self, property):
    has_common_color = len(set(self.colors).intersection(property.colors)) > 0
    at_least_one_non_wild = self.numberOfProperties() == 0 or (len(self.colors) == 1 or len(property.colors) == 1)
    if has_common_color and at_least_one_non_wild and not self.isCompleted():
      self.properties.append(property)
      self.colors = list(set(self.colors).intersection(property.colors))
    else:
      print("Tried to add property. Blocked.")
      print("Property colors: " + str(property.colors))
      print("Set colors: " + str(self.colors))
      print("Has common color? " + str(has_common_color))
      print("At least one non wild? " + str(at_least_one_non_wild))
      print("Set Completed? " + str(self.isCompleted()))
      print("Number to complete: " + str(self.numberToComplete()))
      print("Number in this: " + str(self.numberOfProperties()))
      print("Is defined? " + str(self.isDefined()))

  def numberOfProperties(self):
    return len(self.properties)

  def rentValue(self):
    rent = 0
    if self.isDefined():
      if self.colors[0] == BROWN_PROPERTY:
        rent = len(self.properties)
      elif self.colors[0] == DARK_BLUE_PROPERTY:
        rent = 3 if len(self.properties) == 1 else 8
      elif self.colors[0] == GREEN_PROPERTY:
        rent = 2 * len(self.properties) if len(self.properties) <= 2 else 7
      elif self.colors[0] == LIGHT_BLUE_PROPERTY:
        rent = len(self.properties)
      elif self.colors[0] == ORANGE_PROPERTY:
        rent = 2 * len(self.properties) - 1
      elif self.colors[0] == PINK_PROPERTY:
        rent = 2 ** (len(self.properties) - 1)
      elif self.colors[0] == BLACK_PROPERTY:
        rent = len(self.properties)
      elif self.colors[0] == RED_PROPERTY:
        rent = len(self.properties) + 1 if len(self.properties) <= 2 else 6
      elif self.colors[0] == LIGHT_GREEN_PROPERTY:
        rent = len(self.properties)
      elif self.colors[0] == YELLOW_PROPERTY:
        rent = 2 * len(self.properties)

    return rent + (3 if self.hasHouse else 0) + (4 if self.hasHotel else 0)

  def numberToComplete(self):
    if self.isDefined():
      if self.colors[0] == BROWN_PROPERTY or self.colors[0] == DARK_BLUE_PROPERTY or\
         self.colors[0] == LIGHT_GREEN_PROPERTY:
        return 2
      elif self.colors[0] == GREEN_PROPERTY or self.colors[0] == LIGHT_BLUE_PROPERTY or\
           self.colors[0] == ORANGE_PROPERTY or self.colors[0] == PINK_PROPERTY or\
           self.colors[0] == RED_PROPERTY or self.colors[0] == YELLOW_PROPERTY:
        return 3
      elif self.colors[0] == BLACK_PROPERTY:
        return 4
    else:
      p = [PropertySet(self.colors[i]) for i in range(len(self.colors))]
      return max([x.numberToComplete() for x in p])

  def addHouse(self):
    if self.isCompleted() and self.isDefined() and not self.isUtility():
      self.hasHouse = True
    else:
      print("Couldn't add house")

  def addHotel(self):
    if self.hasHouse:
      self.hasHotel = True
    else:
      print("Tried to add Hotel in non House set")

  def isCompleted(self):
    return self.isDefined() and self.numberOfProperties() >= self.numberToComplete()

  def isDefined(self):
    return len(self.colors) == 1

  def isUtility(self):
    return self.colors[0] == BLACK_PROPERTY or self.colors[0] == LIGHT_GREEN_PROPERTY

  def canAddProperty(self, property):
    has_common_color = len(set(self.colors).intersection(property.colors)) > 0
    at_least_one_non_wild = self.numberOfProperties() == 0 or (len(self.colors) == 1 or len(property.colors) == 1)
    return has_common_color and at_least_one_non_wild and not self.isCompleted()
