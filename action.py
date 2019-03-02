class PlayPropertyAction:
  def __init__(self, property, propertySet):
    self.property = property
    self.propertySet = propertySet

class AddMoneyAction:
  def __init__(self, money):
    self.money = money

class AskMoneyAction:
  def __init__(self, money, targets):
    self.money = money
    self.targets = targets

class DrawCardsAction:
  def __init__(self, quantity):
    self.quantity = quantity

class AddHouseHotelAction:
  def __init__(self, set, house):
    self.set = set
    self.house = house

class StealPropertyAction:
  def __init__(self, property, owner):
    self.property = property
    self.owner = owner

class StealPropertySetAction:
  def __init__(self, set, owner):
    self.set = set
    self.owner = owner

class SwapPropertyAction:
  def __init__(self, mine, other, other_id):
    self.mine = mine
    self.other = other
    self.other_id = other_id

class ApplyDoubleRent:
  def __init__(self):
    self.a = 0
