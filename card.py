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

class PropertySet:
  def __init__(self, colors):
    self.properties = []
    self.colors = colors
    self.hasHouse = False
    self.hasHotel = False

  def addProperty(self, property):
    has_common_color = len(set(self.colors).intersection(property.colors)) > 0
    at_least_one_non_wild = len(self.colors) == 1 or len(property.colors) == 1
    if has_common_color and at_least_one_non_wild and not self.isCompleted():
      self.properties.append(property)
      self.colors = list(set(self.colors).intersection(property.colors))
    else:
      print("Tried to add property. Blocked.")

  def numberOfProperties(self):
    return len(properties)

  def rentValue(self):
    rent = 0
    if self.color == BROWN_PROPERTY:
      rent = len(self.properties)
    elif self.color == DARK_BLUE_PROPERTY:
      rent = 3 if len(self.properties) == 1 else 8
    elif self.color == GREEN_PROPERTY:
      rent = 2 * len(self.properties) if len(self.properties) <= 2 else 7
    elif self.color == LIGHT_BLUE_PROPERTY:
      rent = len(self.properties)
    elif self.color == ORANGE_PROPERTY:
      rent = 2 * len(self.properties) - 1
    elif self.color == PINK_PROPERTY:
      rent = 2 ** (len(self.properties) - 1)
    elif self.color == BLACK_PROPERTY:
      rent = len(self.properties)
    elif self.color == RED_PROPERTY:
      rent = len(self.properties) + 1 if len(self.properties) <= 2 else 6
    elif self.color == LIGHT_GREEN_PROPERTY:
      rent = len(self.properties)
    elif self.color == YELLOW_PROPERTY:
      rent = 2 * len(self.properties)
    return rent + (3 if self.hasHouse else 0) + (4 if self.hasHotel else 0)

  def numberToComplete(self):
    if self.color == BROWN_PROPERTY or self.color == DARK_BLUE_PROPERTY or
       self.color == LIGHT_GREEN_PROPERTY:
      return 2
    elif self.color == GREEN_PROPERTY or self.color == LIGHT_BLUE_PROPERTY or
         self.color == ORANGE_PROPERTY or self.color == PINK_PROPERTY or
         self.color == RED_PROPERTY or self.color == YELLOW_PROPERTY:
      return 3
    elif self.color == BLACK_PROPERTY:
      return 4
    else:
      return -1

  def addHouse(self):
    if self.isCompleted() and self.isDefined() and not self.isUtility():
      self.hasHouse = True
    else
      print("Couldn't add house")

  def addHotel(self):
    if self.hasHouse:
      self.hasHotel = True
    else:
      print("Tried to add Hotel in non House set")

  def isCompleted(self):
    return self.isDefined() and self.numberToComplete() >= self.numberOfProperties()

  def isDefined(self):
    return len(self.colors) == 1

  def isUtility(self):
    return self.colors[0] == BLACK_PROPERTY or self.colors[0] == LIGHT_GREEN_PROPERTY

  def canAddProperty(self, property):
    return not self.isCompleted() and (self.isDefined() or len(property.colors) == 1)
