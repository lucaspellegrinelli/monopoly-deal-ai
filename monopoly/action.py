class Action:
  def __init__(self, who_used):
    self.who_used = who_used

class DoNothingAction(Action):
  def __init__(self, who_used):
    Action.__init__(self, who_used)

  def __repr__(self):
    return "Nothing"

class PlayPropertyAction(Action):
  def __init__(self, who_used, property, propertySet):
    Action.__init__(self, who_used)
    self.property = property
    self.propertySet = propertySet

  def __repr__(self):
    return "Played " + self.property.name + " into a pSet with " + str(len(self.propertySet.properties)) + " properties"

class AddMoneyAction(Action):
  def __init__(self, who_used, money):
    Action.__init__(self, who_used)
    self.money = money

  def __repr__(self):
    return "Added " + str(self.money) + " to the money pile"

class AskMoneyAction(Action):
  def __init__(self, who_used, card, money, targets):
    Action.__init__(self, who_used)
    self.card = card
    self.money = money
    self.targets = targets

  def __repr__(self):
    return "Asked " + str(self.money) + " for " + str(len(self.targets)) + " players"

class DrawCardsAction(Action):
  def __init__(self, who_used, card, quantity):
    Action.__init__(self, who_used)
    self.card = card
    self.quantity = quantity

  def __repr__(self):
    return "Drew " + str(self.quantity) + " cards"

class AddHouseHotelAction(Action):
  def __init__(self, who_used, card, pSet, house):
    Action.__init__(self, who_used)
    self.card = card
    self.pSet = pSet
    self.house = house

  def __repr__(self):
    return "Added a " + ("House" if self.house else "Hotel") + " to a set"

class StealPropertyAction(Action):
  def __init__(self, who_used, card, property, owner):
    Action.__init__(self, who_used)
    self.card = card
    self.property = property
    self.owner = owner

  def __repr__(self):
    return "Stole " + str(self.property.name) + " property from player #" + str(self.owner)

class StealPropertySetAction(Action):
  def __init__(self, who_used, card, pSet, owner):
    Action.__init__(self, who_used)
    self.card = card
    self.pSet = pSet
    self.owner = owner

  def __repr__(self):
    return "Stole pSet with " + str(len(self.pSet.properties)) + " properties from player #" + str(self.owner)

class SwapPropertyAction(Action):
  def __init__(self, who_used, card, mine, other, other_id):
    Action.__init__(self, who_used)
    self.card = card
    self.mine = mine
    self.other = other
    self.other_id = other_id

  def __repr__(self):
    return "Swapped " + str(self.mine.name) + " to " + str(self.other.name)

class ApplyDoubleRent(Action):
  def __init__(self, who_used, card):
    Action.__init__(self, who_used)
    self.card = card

  def __repr__(self):
    return "Applied Double Rent"
