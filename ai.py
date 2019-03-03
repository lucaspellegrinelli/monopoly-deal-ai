from cardsdb import *
from action import *

class AI:
  def __init__(self):
    self.depth = 3

  def getTurnPossibleMoves(self, instance, player):
    moves = []
    moves.append(DoNothingAction())

    other_players_id = []
    other_players = []
    for p in instance.players:
      if p.id != player.id:
        other_players_id.append(p.id)
        other_players.append(p)

    for card in player.hand:
      if isinstance(card, PropertyCard):
        if not card.isRainbow():
          moves.append(PlayPropertyAction(card, PropertySet(card.colors)))
        for pSet in player.sets:
          if pSet.canAddProperty(card):
            moves.append(PlayPropertyAction(card, pSet))
      elif isinstance(card, MoneyCard):
        moves.append(AddMoneyAction(card))
      elif isinstance(card, RentCard):
        moves.append(AddMoneyAction(card))
        for pSet in player.sets:
          if pSet.isDefined() and pSet.rentValue() > 0:
            if card.wild:
              for opid in other_players_id:
                moves.append(AskMoneyAction(card, pSet.rentValue() * (2 if player.doubleRent else 1), [opid]))
            elif pSet.colors[0] in card.colors:
              moves.append(AskMoneyAction(card, pSet.rentValue() * (2 if player.doubleRent else 1), other_players_id))
      elif isinstance(card, ActionCard):
        moves.append(AddMoneyAction(card))
        if card.id == DEBT_COLLECTOR:
          # Force someone to give you 5M
          for op in other_players:
            moves.append(AskMoneyAction(card, 5, [op]))
        elif card.id == ITS_MY_BIRTHDAY:
          # Get 2M from everyone
          moves.append(AskMoneyAction(card, 2, other_players))
        elif card.id == PASS_GO:
          # Draws 2 cards
          moves.append(DrawCardsAction(card, 2))
        elif card.id == HOUSE:
          # Increases rent value for completed set
          for pSet in player.sets:
            if pSet.isCompleted() and not pSet.isUtility():
              moves.append(AddHouseHotelAction(card, pSet, True))
        elif card.id == HOTEL:
          # Increases rent value for houses
          for pSet in player.sets:
            if pSet.hasHouse:
              moves.append(AddHouseHotelAction(card, pSet, False))
        elif card.id == SLY_DEAL:
          # Steals a single property from a non completed set
          for op in other_players:
            for pSet in op.sets:
              if not pSet.isCompleted():
                for property in pSet.properties:
                  moves.append(StealPropertyAction(card, property, op.id))
        elif card.id == DEAL_BREAKER:
          # Steals a completed property set
          for op in other_players:
            for pSet in op.sets:
              if pSet.isCompleted():
                moves.append(StealPropertySetAction(card, pSet, op.id))
        elif card.id == FORCED_DEAL:
          # Forces swap between one of your properties and someone elses property
          my_properties = []
          other_properties = []
          for mySet in player.sets:
            if not mySet.isCompleted() and mySet.numberOfProperties() > 0:
              my_properties += [p for p in mySet.properties]

          for otherPlayer in other_players:
            for otherSet in otherPlayer.sets:
              if not otherSet.isCompleted() and otherSet.numberOfProperties() > 0:
                other_properties += [[p, otherPlayer.id] for p in otherSet.properties]

          for myP in my_properties:
            for otherP in other_properties:
              moves.append(SwapPropertyAction(card, myP, otherP[0], otherP[1]))
        elif card.id == DOUBLE_RENT:
          # Doubles the next rent card played this turn
          moves.append(ApplyDoubleRent(card))

    return moves
