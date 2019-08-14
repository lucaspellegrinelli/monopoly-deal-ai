from flags import *

# Class responsible for managing what a general card should have
class Card:
  def __init__(self, id, name, value):
    self.id = id
    self.name = name
    self.value = value

  def __repr__(self):
    return self.name

# Class responsible for managing what (besides what's already defined in the Card class)
# is necessary for a Money Card
class MoneyCard(Card):
  def __init__(self, id, name, value):
    Card.__init__(self, id, name, value)

# Class responsible for managing what (besides what's already defined in the Card class)
# is necessary for a Action Card (examples of Action Cards are like 'Deal Breaker' or
# 'Debt Collector')
class ActionCard(Card):
  def __init__(self, id, name, value, action):
    Card.__init__(self, id, name, value)
    self.action = action

# Class responsible for managing what (besides what's already defined in the Card class)
# is necessary for a Property Card (that could have multiple colors)
class PropertyCard(Card):
  def __init__(self, id, name, value, colors):
    Card.__init__(self, id, name, value)
    self.colors = colors

  def isRainbow(self):
    return self.colors[0] == 10

# Class responsible for managing what (besides what's already defined in the Card class)
# is necessary for a Rent Card (including multiple colors rent and wild rent)
class RentCard(Card):
  def __init__(self, id, name, value, colors, wild):
    Card.__init__(self, id, name, value)
    self.colors = colors
    self.wild = wild

# Class corresponding to a card that the target player doesn't have information about
# like in the case of other players hand or the deck
class UnknownCard(Card):
  def __init__(self):
    Card.__init__(self, -1, "Unknown", -1)