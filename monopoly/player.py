import random
import copy

from property_set import PropertySet

from cardsdb import *
from action import *

class Player:
  def __init__(self, id, hand, ai):
    self.id = id
    self.hand = hand
    self.sets = []
    self.money = []

    self.ai = ai

    self.doubleRent = False

  def chooseMove(self, instance, moves_left):
    move = self.ai.chooseMove(instance, self.id, moves_left)

    if not isinstance(move, Action):
      move = DoNothingAction()

    return move

  def choosePayment(self, instance, how_much):
    payment = []
    payed = 0

    while payed < how_much and len(self.money) > 0 and len(self.sets) > 0:
      this_it_pay = self.ai.choosePayment(instance, self.id, how_much)

      if len(this_it_pay) == 0:
        raise RuntimeError("The method 'choosePayment' didn't choose enough cards \
        to pay the required amount even tough it has more cards and in this iteration \
        it didn't return any cards. This might be a sign of an infinite loop where \
        'choosePayment' will never finish to choose the payment since it will not \
        make any more actions (based on the fact that in this iteration it didn't).")

      payment += this_it_pay

      for card in payment:
        payed += card.value
        if isinstance(card, PropertyCard):
          for set in self.sets:
            if set.hasProperty(card):
              set.removeProperty(card)
              break
        else:
          self.removeFromMoneyPile(card)

    self.cleanClearSets()
    return payment

  def chooseWhatToDiscard(self, instance):
    discarded = []
    while len(self.hand) > 7:
      discarded += self.ai.chooseWhatToDiscard(instance, self.id)

      if len(discarded) == 0:
        raise RuntimeError("You didn't discard enough in the 'chooseWhatToDiscard' \
        and in this iteration the discard list is empty. This might be a \
        sign of an infinite loop where 'chooseWhatToDiscard' will never finish to \
        discard the necessary cards since it will not make any more actions (based \
        on the fact that in this iteration it didn't).")

      for card in discarded:
        self.removeFromHand(card)

    return discarded

  def recievePayment(self, instance, payment):
    single_properties = []
    for item in payment:
      if isinstance(item, MoneyCard) or isinstance(item, ActionCard) or isinstance(item, RentCard):
        self.money.append(item)
      elif isinstance(item, PropertyCard):
        single_properties.append(item)
      elif isinstance(item, PropertySet):
        self.sets.append(item)

    if single_properties:
      actions = self.ai.recievePayment(instance, self.id, single_properties)

      if len(actions) == 0:
        raise RuntimeError("There are properties unaddressed in 'recievePayment' \
        and in this iteration the method didn't make any actions. This might be a \
        sign of an infinite loop where 'recievePayment' will never finish to \
        address all the properties since it will not make any more actions (based \
        on the fact that in this iteration it didn't).")

      addressed_cards = []
      addressed_cards_id = []
      for action in actions:
        addressed_cards.append(action.property)
        addressed_cards_id.append(action.property.id)
        self.addToPropertySet(action.property_set, action.property)

      unaddressed_cards = [p for p in single_properties if p.id not in addressed_cards_id]

      if len(unaddressed_cards) > 0:
        self.recievePayment(instance, unaddressed_cards)

  def willNegate(self, instance, action):
    has_negate = len([c for c in self.hand if c.id == JUST_SAY_NO]) > 0

    if has_negate:
      negate = self.ai.willNegate(instance, self.id, action)
      if negate != True and negate != False:
        raise RuntimeError("In the 'willNegate' method, the return value was not a boolean.")
      return negate
    else:
      return False

  def turnPassing(self):
    self.doubleRent = False
    self.cleanClearSets()

  def cleanClearSets(self):
    self.sets = [x for x in self.sets if x.numberOfProperties() > 0]

  def addToHand(self, cards):
    self.hand += cards

  # TODO: MAKE THIS WORK WITH "self.hand.remove(card)"
  def removeFromHand(self, card):
    for c in self.hand:
      if c.id == card.id:
        self.hand.remove(c)
        break

  def addPropertySet(self, set):
    self.sets.append(set)

  def removePropertySet(self, set):
    self.sets.remove(set)

  def hasPropertySet(self, set):
    return set in self.sets

  def addToPropertySet(self, set, card):
    if set.numberOfProperties() > 0:
      for s in self.sets:
        if s.id == set.id:
          s.addProperty(card)
          return
    else:
      pSet = PropertySet(set.colors)
      pSet.addProperty(card)
      self.addPropertySet(pSet)

  def addToMoneyPile(self, card):
    self.money.append(card)

  # TODO: MAKE THIS WORK WITH "self.money.remove(card)"
  def removeFromMoneyPile(self, card):
    for c in self.money:
      if c.id == card.id:
        self.money.remove(c)
        break

  def removeGeneralProperty(self, property):
    for set in self.sets:
      if set.hasProperty(property):
        set.removeProperty(property)
        return

  def hasWon(self):
    completed = 0
    for set in self.sets:
      if set.isCompleted():
        completed += 1

    return completed >= 3

  def copy(self):
    return copy.deepcopy(self)

  def __str__(self):
    final = "\n- Hand :\t" + str(self.hand) + "\n"
    final += "- Money:\t" + str(self.money) + "\n"
    final += "- Field:\t" + str(self.sets) + "\n"

    return final
