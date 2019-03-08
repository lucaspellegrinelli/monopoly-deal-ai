from cardsdb import *
from ai import *
import random
import copy

class Player:
  def __init__(self, id, hand):
    self.id = id
    self.hand = hand
    self.sets = []
    self.money = []

    self.ai = AI()

    self.doubleRent = False

  def addToHand(self, cards):
    self.hand += cards

  def removeFromHand(self, card):
    for c in self.hand:
      if c.id == card.id:
        self.hand.remove(c)
        break

  def addPropertySet(self, set):
    self.sets.append(set)

  def removePropertySet(self, set):
    for s in self.sets:
      if s.id == set.id:
        self.sets.remove(s)
        break

  def hasPropertySet(self, set):
    for s in self.sets:
      if s.id == set.id:
        return True
    return False

  def addToMoneyPile(self, card):
    self.money.append(card)

  def removeFromMoneyPile(self, card):
    for c in self.money:
      if c.id == card.id:
        self.money.remove(c)
        break

  def chooseMove(self, instance, moves_left):
    return self.ai.randomChooseMove(self, instance)

  def choosePayment(self, instance, how_much):
    ans = self.ai.randomChoosePayment(self, how_much)
    self.cleanClearSets()
    return ans

  def chooseWhatToDiscard(self, instance):
    return self.ai.randomChooseWhatToDiscard(self)

  def recievePayment(self, instance, payment):
    single_properties = []
    for item in payment:
      if isinstance(item, MoneyCard) or isinstance(item, ActionCard) or isinstance(item, RentCard):
        self.money.append(item)
      elif isinstance(item, PropertyCard):
        single_properties.append(item)
      elif isinstance(item, PropertySet):
        self.sets.append(item)

    self.ai.randomRecievePayment(self, single_properties)

  def willNegate(self, instance):
    return self.ai.randomWillNegate(self)

  def turnPassing(self):
    self.doubleRent = False
    self.cleanClearSets()

  def cleanClearSets(self):
    if self.sets != []:
      for i in range(len(self.sets) - 1, -1, -1):
        if self.sets[i] == [] or self.sets[i].numberOfProperties() == 0:
          del self.sets[i]

  def __str__(self):
    final = "Hand:\t" + str(self.hand) + "\n"
    final += "Money:\t" + str(self.money) + "\n"
    final += "Field:\t" + str(self.sets) + "\n"

    return final
