import random

from ..cardsdb import *
from ..action import *
from ..property_set import *

from ..ai import AI

# Example of an implemented AI that does random stuff for living
class RandomAI(AI):

  def chooseMove(self, instance, player, moves_left):
    possible_moves = instance.getTurnPossibleMoves(player)
    return possible_moves[random.randint(0, len(possible_moves) - 1)]

  def choosePayment(self, instance, player, how_much):
    payment = []
    payed = 0

    for item in player.money:
      if payed < how_much:
        payed += item.value
        payment.append(copy.deepcopy(item))

    for pSet in player.sets:
      for item in pSet.properties:
        if payed < how_much:
          payed += item.value
          payment.append(copy.deepcopy(item))
        else:
          break

    return payment

  def chooseWhatToDiscard(self, instance, player):
    discarded = []
    while len(player.hand) > 7:
      discarded.append(player.hand.pop(random.randint(0, len(player.hand) - 1)))
    return discarded

  def recievePayment(self, instance, player, properties):
    actions = []

    for item in properties:
      added = False
      for pSet in player.sets:
        if pSet.canAddProperty(item):
          actions.append(PlayPropertyAction(item, pSet))
          added = True
          break

      if not added:
        actions.append(PlayPropertyAction(item, PropertySet(item.colors)))

    return actions

  def willNegate(self, instance, player):
    has_negate = False
    for card in player.hand:
      if card != [] and card.id == JUST_SAY_NO:
        has_negate = True
        break
    return has_negate
