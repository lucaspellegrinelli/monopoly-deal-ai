import cardconsts

class Card:
  def __init__(self, id, name, type, value):
    self.id = id
    self.type  = type
    self.name = name
    self.value = value

class MoneyCard(Card):
  def __init__(self, id, name, value):
    Card.__init__(self, id, name, MONEY_CARD, value)

class ActionCard(Card):
  def __init__(self, id, name, value, action):
    Card.__init__(self, id, name, ACTION_CARD, value)
    self.action = action

class PropertyCard(Card):
  def __init__(self, id, name, value, colors):
    Card.__init__(self, id, name, PROPERTY_CARD, value)
    self.colors = colors

class RentCard(Card):
  def __init__(self, id, name, value, colors, wild):
    Card.__init__(self, id, name, PROPERTY_CARD, value)
    self.colors = colors
    self.wild = wild
