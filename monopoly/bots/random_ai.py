import random

from ..cardsdb import *
from ..action import *
from ..property_set import *

from ..ai import AI

# Example of an implemented AI that does random stuff for living
class RandomAI(AI):

  def chooseMove(self, instance, player_id, moves_left):
    possible_moves = instance.getTurnPossibleMoves(instance.getPlayer(player_id))
    return possible_moves[random.randint(0, len(possible_moves) - 1)]

  def choosePayment(self, instance, player_id, player_sets, player_money_pile, how_much):
    payment = []
    payed = 0

    for item in player_money_pile:
      if payed < how_much:
        payed += item.value
        payment.append(item)

    for p_set in player_sets:
      for item in p_set.properties:
        if payed < how_much:
          payed += item.value
          payment.append(item)
        else:
          break

    return payment

  def chooseWhatToDiscard(self, instance, player_id, player_hand):
    player = instance.getPlayer(player_id)
    discarded = []
    while len(player_hand) > 7:
      discarded.append(player_hand.pop(random.randint(0, len(player_hand) - 1)))
    return discarded

  def recievePropertiesFromPayment(self, instance, player_id, properties):
    player = instance.getPlayer(player_id)
    actions = []

    for item in properties:
      added = False
      for pSet in player.sets:
        if pSet.canAddProperty(item):
          actions.append(PlayPropertyAction(player, item, pSet))
          added = True
          break

      if not added:
        actions.append(PlayPropertyAction(player, item, PropertySet(item.colors)))

    return actions

  def willNegate(self, instance, player_id, action):
    if isinstance(action, AskMoneyAction):
      return True
    elif isinstance(action, StealPropertyAction):
      return False
    elif isinstance(action, StealPropertySetAction):
      return True
    elif isinstance(action, SwapPropertyAction):
      return False
    else:
      return False

  def arrangeWildcards(self, instance, player_id, player_sets):
    actions = []
    wild_cards = []
    for set in player_sets:
      if not set.isDefined():
        wild = (set.properties[0], set)
        wild_cards.append(wild)

    for wild in wild_cards:
      added = False
      for set in player_sets:
        if set.canAddProperty(wild[0]):
          actions.append(MovePropertyAction(player_id, wild[0], wild[1], set))
          break

    return actions
