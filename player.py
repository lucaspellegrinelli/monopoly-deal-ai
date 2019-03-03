from cardsdb import *
import random
import copy

class Player:
  def __init__(self, id, hand):
    self.id = id
    self.hand = hand
    self.sets = []
    self.money = []

    self.doubleRent = False

  def chooseMove(self, instance, possible_moves, moves_left):
    # Dumb
    if possible_moves:
      self.cleanClearSets()
      return possible_moves[random.randint(0, len(possible_moves) - 1)]
    else:
      print("Problem with the possible moves. Quitting.")
      quit()

  def choosePayment(self, instance, how_much):
    # Naive
    payment = []
    payed = 0
    for money in self.money:
      if payed < how_much:
        payed += money.value
        payment.append(copy.deepcopy(money))
        self.money.remove(money)
      else:
        break

    for pSet in self.sets:
      if payed >= how_much:
        break
      for property in pSet.properties:
        if payed < how_much:
          payed += property.value
          payment.append(copy.deepcopy(property))
          pSet.properties.remove(property)
        else:
          break

    self.cleanClearSets()
    print(self.id, payment)
    return payment

  def chooseWhatToDiscard(self, instance):
    #Naive
    discarded = []
    while len(self.hand) > 7:
      discarded.append(self.hand.pop(random.randint(0, len(self.hand) - 1)))

    return discarded

  def recievePayment(self, payment):
    # Naive
    for card in payment:
      if isinstance(card, MoneyCard) or isinstance(card, ActionCard) or isinstance(card, RentCard):
        self.money.append(card)
      elif isinstance(card, PropertyCard):
        added = False
        for pSet in self.sets:
          if pSet.canAddProperty(card):
            pSet.addProperty(card)
            added = True
            break

        if not added:
          pSet = PropertySet(card.colors)
          pSet.addProperty(card)
          self.sets.append(pSet)
      elif isinstance(card, PropertySet):
        self.sets.append(card)
      else:
        print("?????")

    self.cleanClearSets()

  def willNegate(self, instance):
    has_negate = False
    for card in self.hand:
      if card != [] and card.id == JUST_SAY_NO:
        has_negate = True
        break
    return has_negate

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

  def printInfo(self):
    hand_str = ""
    for card in self.hand:
      if card != []:
        hand_str += "[" + str(card.name) + "] "
    print("Player #" + str(self.id) + " Hand:\n" + hand_str + "\n")

    money_str = ""
    for money in self.money:
      money_str += "[" + str(money.name) + "] "
    print("Player #" + str(self.id) + " Money Pile:\n" + money_str + "\n")

    sets_str = ""
    for pSet in self.sets:
      sets_str += "["
      for p in pSet.properties:
        sets_str += "[" + str(p.name) + "]"
      sets_str += "]\n"
    print("Player #" + str(self.id) + " Field:\n" + sets_str + "\n")
