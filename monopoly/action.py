class Action:
  pass

class DoNothingAction(Action):
  def __repr__(self):
    return "Nothing"

class PlayPropertyAction(Action):
  def __init__(self, property, propertySet):
    self.property = property
    self.propertySet = propertySet

  def __repr__(self):
    return "Played " + self.property.name + " into a pSet with " + str(len(self.propertySet.properties)) + " properties"

class AddMoneyAction(Action):
  def __init__(self, money):
    self.money = money

  def __repr__(self):
    return "Added " + str(self.money) + " to the money pile"

class AskMoneyAction(Action):
  def __init__(self, card, money, targets):
    self.card = card
    self.money = money
    self.targets = targets

  def __repr__(self):
    return "Asked " + str(self.money) + " for " + str(len(self.targets)) + " players"

class DrawCardsAction(Action):
  def __init__(self, card, quantity):
    self.card = card
    self.quantity = quantity

  def __repr__(self):
    return "Drew " + str(self.quantity) + " cards"

class AddHouseHotelAction(Action):
  def __init__(self, card, pSet, house):
    self.card = card
    self.pSet = pSet
    self.house = house

  def __repr__(self):
    return "Added a " + ("House" if self.house else "Hotel") + " to a set"

class StealPropertyAction(Action):
  def __init__(self, card, property, owner):
    self.card = card
    self.property = property
    self.owner = owner

  def __repr__(self):
    return "Stole " + str(self.property.name) + " property from player #" + str(self.owner)

class StealPropertySetAction(Action):
  def __init__(self, card, pSet, owner):
    self.card = card
    self.pSet = pSet
    self.owner = owner

  def __repr__(self):
    return "Stole pSet with " + str(len(self.pSet.properties)) + " properties from player #" + str(self.owner)

class SwapPropertyAction(Action):
  def __init__(self, card, mine, other, other_id):
    self.card = card
    self.mine = mine
    self.other = other
    self.other_id = other_id

  def __repr__(self):
    return "Swapped " + str(self.mine.name) + " to " + str(self.other.name)

class ApplyDoubleRent(Action):
  def __init__(self, card):
    self.card = card

  def __repr__(self):
    return "Applied Double Rent"
