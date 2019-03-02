class PlayPropertyAction:
  def __init__(self, property, propertySet):
    self.property = property
    self.propertySet = propertySet

class AddMoneyAction:
  def __init__(self, money):
    self.money = money

class UseRentAction:
  def __init__(self, colors, actualColor, wild):
    self.colors = colors
    self.actualColor = actualColor
    self.wild = wild

class UseActionCard:
  def __init__(self, action):
    self.action = action
