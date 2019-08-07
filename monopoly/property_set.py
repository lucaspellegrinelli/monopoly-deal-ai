import random

from card import *

class PropertySet:
  def __init__(self, colors):
    self.id = random.randint(-9999999, 9999999) # Probably there's a better option
    self.properties = []
    self.colors = colors
    self.hasHouse = False
    self.hasHotel = False



  # ======================== PROPERTY MANAGEMENT ========================

  def addProperty(self, property):
    if self.canAddProperty(property):
      self.properties.append(property)
      self.colors = list(set(self.colors).intersection(property.colors))

  def canAddProperty(self, property):
    has_common_color = len(set(self.colors).intersection(property.colors)) > 0
    at_least_one_non_wild = self.numberOfProperties() == 0 or (len(self.colors) == 1 or len(property.colors) == 1)
    return has_common_color and at_least_one_non_wild and not self.isCompleted()

  def removeProperty(self, property):
    # TODO: MAKE THIS WORK WITH "self.properties.remove(property)"
    for p in self.properties:
      if p.id == property.id:
        self.properties.remove(p)
        break

  def hasProperty(self, property):
    # TODO: MAKE THIS WORK WITH "property in self.properties"
    for p in self.properties:
      if p.id == property.id:
        return True
    return False



  # ======================== UTIL ========================

  def numberOfProperties(self):
    return len(self.properties)

  # Returns the value of the current property set that will be used
  # as the rent value
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

  # Returns the number of properties that this property set needs for it to be completed
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
      # If there's only a multi color property, we will assume the maximum number it needs
      # based on the colors available on this multi color property
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



  # ======================== TESTS ========================
  def isCompleted(self):
    return self.isDefined() and self.numberOfProperties() >= self.numberToComplete()

  def isDefined(self):
    return len(self.colors) == 1 and self.colors[0] != RAINBOW_PROPERTY

  def isUtility(self):
    return self.colors[0] == BLACK_PROPERTY or self.colors[0] == LIGHT_GREEN_PROPERTY



  # ======================== BUILT IN METHODS OVERRIDE ========================
  def __repr__(self):
    return str(self.properties)

  def __eq__(self, other):
    return self.id == other.id

  def __ne__(self, other):
    return not self.__eq__(other)
