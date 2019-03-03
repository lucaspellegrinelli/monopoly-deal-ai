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
    rem = []
    for pSet in self.sets:
      if pSet.numberOfProperties() == 0:
        rem.append(pSet)

    for pSet in rem:
      self.sets.remove(pSet)

  def __str__(self):
    final = ""

    hand_str = ""
    for card in self.hand:
      if card != []:
        hand_str += "[" + str(card.name) + "] "

    final += "Player #" + str(self.id) + " Hand:\n" + hand_str + "\n"

    money_str = ""
    for money in self.money:
      money_str += "[" + str(money.name) + "] "

    final += "Player #" + str(self.id) + " Money Pile:\n" + money_str + "\n"

    sets_str = ""
    for pSet in self.sets:
      sets_str += "["
      for p in pSet.properties:
        sets_str += "[" + str(p.name) + "]"
      sets_str += "]\n"

    final += "Player #" + str(self.id) + " Field:\n" + sets_str + "\n"

    return final
