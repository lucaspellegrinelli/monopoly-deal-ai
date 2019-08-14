# Abstract class representing all various actions a player can execute
class Action:
  def __init__(self, who_used_id):
    self.who_used_id_id = who_used_id

# Class representing the action of not playing any cards
class DoNothingAction(Action):
  def __init__(self, who_used_id):
    Action.__init__(self, who_used_id)

  def __repr__(self):
    return "Nothing"

# Class representing the action of a target player playing a property
# into a property set
class PlayPropertyAction(Action):
  def __init__(self, who_used_id, property, property_set):
    Action.__init__(self, who_used_id)
    self.property = property
    self.property_set = property_set

  def __repr__(self):
    return "Played " + self.property.name + " into a pSet with " + str(len(self.property_set.properties)) + " properties"

# Class representing the action of a target player moving a property
# between two property sets
class MovePropertyAction(Action):
  def __init__(self, who_used_id, property, property_set_bef, property_set_aft):
    Action.__init__(self, who_used_id)
    self.property = property
    self.property_set_bef = property_set_bef
    self.property_set_aft = property_set_aft

  def __repr__(self):
    return "Removed " + self.property.name + " into a pSet with " + str(len(self.property_set.properties)) + " properties"

# Class representing the action of a target player adding a card to
# its money pile
class AddMoneyAction(Action):
  def __init__(self, who_used_id, money):
    Action.__init__(self, who_used_id)
    self.money = money

  def __repr__(self):
    return "Added " + str(self.money) + " to the money pile"

# Class representing the action of a target player resolving the effect
# of a card that requires one or more other players to give it a specified
# amount of money
class AskMoneyAction(Action):
  def __init__(self, who_used_id, card, money, targets):
    Action.__init__(self, who_used_id)
    self.card = card
    self.money = money
    self.targets = targets

  def __repr__(self):
    return "Asked " + str(self.money) + " for Players #" + str(self.targets)

# Class representing the action of a target player drawing a specific
# amount of cards
class DrawCardsAction(Action):
  def __init__(self, who_used_id, card, quantity):
    Action.__init__(self, who_used_id)
    self.card = card
    self.quantity = quantity

  def __repr__(self):
    return "Drew " + str(self.quantity) + " cards"

# Class representing the action of a target player adding a house or hotel
# on top of a specified property set
class AddHouseHotelAction(Action):
  def __init__(self, who_used_id, card, property_set, house):
    Action.__init__(self, who_used_id)
    self.card = card
    self.property_set = property_set
    self.house = house

  def __repr__(self):
    return "Added a " + ("House" if self.house else "Hotel") + " to a set"

# Class representing the action of a target player resolving the effect
# of a card that steals a specified property from another player
class StealPropertyAction(Action):
  def __init__(self, who_used_id, card, property, other_player_id):
    Action.__init__(self, who_used_id)
    self.card = card
    self.property = property
    self.other_player_id = other_player_id

  def __repr__(self):
    return "Stole " + str(self.property.name) + " property from player #" + str(self.other_player_id)

# Class representing the action of a target player resolving the effect
# of a card that steals a specified property set from another player
class StealPropertySetAction(Action):
  def __init__(self, who_used_id, card, property_set, other_player_id):
    Action.__init__(self, who_used_id)
    self.card = card
    self.property_set = property_set
    self.other_player_id = other_player_id

  def __repr__(self):
    return "Stole pSet with " + str(len(self.property_set.properties)) + " properties from player #" + str(self.other_player_id)

# Class representing the action of a target player resolving the effect
# of a card that swaps a specified property with another player
class SwapPropertyAction(Action):
  def __init__(self, who_used_id, card, my_property, other_property, other_player_id):
    Action.__init__(self, who_used_id)
    self.card = card
    self.my_property = my_property
    self.other_property = other_property
    self.other_player_id = other_player_id

  def __repr__(self):
    return "Swapped " + str(self.my_property.name) + " to " + str(self.other_property.name) + " (from Player #" + str(self.other_player_id) + ")"

# Class representing the action of a target player resolving the effect
# of a card that doubles the amount of money that a rent card would require
# from other players
class ApplyDoubleRent(Action):
  def __init__(self, who_used_id, card):
    Action.__init__(self, who_used_id)
    self.card = card

  def __repr__(self):
    return "Applied Double Rent"
