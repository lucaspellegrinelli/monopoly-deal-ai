import copy
import random

from cardsdb import *
from action import *

from player import Player
from property_set import PropertySet
from deck import Deck

class Game:
  def __init__(self, n_players, ai):
    self.actionsPerTurn = 3
    self.startingHandCount = 5
    self.drawPerTurn = 2
    self.completedSetsToWin = 3
    self.ai = ai
    self.noOptionsCount = 0
    self.deck = Deck(ALL_CARDS)
    self.players = [Player(i, self.deck.getCards(self.startingHandCount), ai) for i in range(n_players)]

  def run(self):
    player_index = random.randint(0, len(self.players) - 1)
    game_state = self.getGameState()

    while not game_state.ended:
      print("\n--------- Turn Starting ---------\n")
      player = self.players[player_index]
      print("Player #" + str(player_index) + " turn\n")

      print(player)

      player.addToHand(self.deck.getCards(self.drawPerTurn))
      for action in range(self.actionsPerTurn):
        chosen_action = player.chooseMove(self.getInstance(player), self.actionsPerTurn - action)
        print("[Action] " + str(chosen_action))

        if isinstance(chosen_action, DoNothingAction):
          self.noOptionsCount += 1
        else:
          self.noOptionsCount = 0

        self.applyAction(chosen_action, player)

      game_state = self.getGameState()

      player.turnPassing()
      discarded_cards = player.chooseWhatToDiscard(self.getInstance(player))

      print(player)

      random.shuffle(discarded_cards)
      self.deck.deck += discarded_cards
      player_index = (player_index + 1) % len(self.players)

    return game_state

  def getInstance(self, player):
    instance = Game(len(self.players), self.ai)
    instance.deck = copy.deepcopy(self.deck)
    instance.players = copy.deepcopy(self.players)
    instance.noOptionsCount = copy.deepcopy(self.noOptionsCount)

    # The played doesn't have info about cards in opponent hand
    # So I need to blend it with the deck
    cards_in_hand = []
    for p in instance.players:
      if p.id != player.id:
        cards_in_hand.append([p.id, len(p.hand)])
        instance.deck.deck += copy.deepcopy(p.hand)
        p.hand = []

    instance.deck.shuffle()
    for p in instance.players:
      for c_in_hand in cards_in_hand:
        if p.id == c_in_hand[0]:
          p.hand += instance.deck.getCards(c_in_hand[1])
          break

    return instance

  def getGameState(self):
    if self.noOptionsCount >= len(self.players) * 3:
      return EndGameResult(True, True)

    for player in self.players:
      if player.hasWon():
        return EndGameResult(True, False, player)

    return EndGameResult(False)

  def getTurnPossibleMoves(self, player):
    moves = []
    moves.append(DoNothingAction(player))

    other_players_id = []
    other_players = []
    for p in self.players:
      if p.id != player.id:
        other_players_id.append(p.id)
        other_players.append(p)

    for card in player.hand:
      if isinstance(card, PropertyCard):
        if not card.isRainbow():
          moves.append(PlayPropertyAction(player.id, card, PropertySet(card.colors)))
        for pSet in player.sets:
          if pSet.canAddProperty(card):
            moves.append(PlayPropertyAction(player.id, card, pSet))
      elif isinstance(card, MoneyCard):
        moves.append(AddMoneyAction(player.id, card))
      elif isinstance(card, RentCard):
        moves.append(AddMoneyAction(player.id, card))
        for pSet in player.sets:
          if pSet.isDefined() and pSet.rentValue() > 0:
            if card.wild:
              for opid in other_players_id:
                moves.append(AskMoneyAction(player.id, card, pSet.rentValue() * (2 if player.doubleRent else 1), [opid]))
            elif pSet.colors[0] in card.colors:
              moves.append(AskMoneyAction(player.id, card, pSet.rentValue() * (2 if player.doubleRent else 1), other_players_id))
      elif isinstance(card, ActionCard):
        moves.append(AddMoneyAction(player.id, card))
        if card.id == DEBT_COLLECTOR:
          # Force someone to give you 5M
          for op in other_players:
            moves.append(AskMoneyAction(player.id, card, 5, [op]))
        elif card.id == ITS_MY_BIRTHDAY:
          # Get 2M from everyone
          moves.append(AskMoneyAction(player.id, card, 2, other_players))
        elif card.id == PASS_GO:
          # Draws 2 cards
          moves.append(DrawCardsAction(player.id, card, 2))
        elif card.id == HOUSE:
          # Increases rent value for completed set
          for pSet in player.sets:
            if pSet.isCompleted() and not pSet.isUtility():
              moves.append(AddHouseHotelAction(player.id, card, pSet, True))
        elif card.id == HOTEL:
          # Increases rent value for houses
          for pSet in player.sets:
            if pSet.hasHouse:
              moves.append(AddHouseHotelAction(player.id, card, pSet, False))
        elif card.id == SLY_DEAL:
          # Steals a single property from a non completed set
          for op in other_players:
            for pSet in op.sets:
              if not pSet.isCompleted():
                for property in pSet.properties:
                  moves.append(StealPropertyAction(player.id, card, property, op.id))
        elif card.id == DEAL_BREAKER:
          # Steals a completed property set
          for op in other_players:
            for pSet in op.sets:
              if pSet.isCompleted():
                moves.append(StealPropertySetAction(player.id, card, pSet, op.id))
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
              moves.append(SwapPropertyAction(player.id, card, myP, otherP[0], otherP[1]))
        elif card.id == DOUBLE_RENT:
          # Doubles the next rent card played this turn
          moves.append(ApplyDoubleRent(player.copy(), card))

    return moves

  def applyAction(self, action, player):
    other_players_id = []
    other_players = []
    for p in self.players:
      if p.id != player.id:
        other_players_id.append(p.id)
        other_players.append(p)

    if isinstance(action, PlayPropertyAction):
      pr = copy.deepcopy(action.property)
      if len(action.propertySet.properties) == 0:
        pSet = PropertySet(action.propertySet.colors)
        pSet.addProperty(pr)
        player.addPropertySet(pSet)
      elif player.hasPropertySet(action.propertySet):
        player.addToPropertySet(action.propertySet, pr)

      player.removeFromHand(action.property)

    elif isinstance(action, AddMoneyAction):
      player.addToMoneyPile(action.money)
      player.removeFromHand(action.money)

    elif isinstance(action, AskMoneyAction):
      payments = []
      for p in self.players:
        if p.id in action.targets:
          if p.willNegate(self.getInstance(player), action):
            for c_hand in p.hand:
              if c_hand.id == JUST_SAY_NO:
                self.deck.addToUsedPile(copy.deepcopy(c_hand))
                p.removeFromHand(c_hand)
                break
          else:
            payments += p.choosePayment(self.getInstance(player), action.money)

      self.deck.addToUsedPile(copy.deepcopy(action.card))

      player.removeFromHand(action.card)
      player.recievePayment(self.getInstance(player), payments)

    elif isinstance(action, DrawCardsAction):
      player.hand += self.deck.getCards(action.quantity)
      self.deck.addToUsedPile(copy.deepcopy(action.card))
      player.removeFromHand(action.card)

    elif isinstance(action, AddHouseHotelAction):
      if action.house:
        action.pSet.addHouse()
      else:
        action.pSet.addHotel()

      player.removeFromHand(action.card)

    elif isinstance(action, StealPropertyAction):
      negated = False
      stolen_property = copy.deepcopy(action.property)
      for p in other_players:
        if p.id == action.owner:
          if p.willNegate(self.getInstance(player), action):
            negated = True
            break

          for pSet in p.sets:
            if pSet.hasProperty(action.property):
              pSet.removeProperty(action.property)
              break
          break

      if not negated:
        player.recievePayment(self.getInstance(player), [stolen_property])

      self.deck.addToUsedPile(copy.deepcopy(action.card))
      player.removeFromHand(action.card)

    elif isinstance(action, StealPropertySetAction):
      negated = False
      stolen_set = copy.deepcopy(action.pSet)
      for p in other_players:
        if p.id == action.owner and p.hasPropertySet(action.pSet):
          if p.willNegate(self.getInstance(player), action):
            negated = True
          else:
            p.removePropertySet(action.pSet)
          break

      if not negated:
        player.recievePayment(self.getInstance(player), [stolen_set])

      self.deck.addToUsedPile(copy.deepcopy(action.card))
      player.removeFromHand(action.card)

    elif isinstance(action, SwapPropertyAction):
      negated = False
      stolen_property = copy.deepcopy(action.other)
      my_property = copy.deepcopy(action.mine)

      for pSet in player.sets:
        if pSet.hasProperty(action.mine):
          pSet.removeProperty(action.mine)
          break

      for p in other_players:
        if p.id == action.other_id:
          if p.willNegate(self.getInstance(player), action):
            negated = True
            break

          for pSet in p.sets:
            if pSet.hasProperty(action.other):
              pSet.removeProperty(action.other)
              break

          if not negated:
            p.recievePayment(self.getInstance(player), [my_property])

      if not negated:
        player.recievePayment(self.getInstance(player), [stolen_property])

      self.deck.addToUsedPile(copy.deepcopy(action.card))
      player.removeFromHand(action.card)

    elif isinstance(action, ApplyDoubleRent):
      player.doubleRent = True
      self.deck.used_pile.append(copy.deepcopy(action.card))
      player.removeFromHand(action.card)

  def getPlayer(self, player_id):
    for p in self.players:
      if p.id == player_id:
        return p

  def printCardQtdInfo(self):
    print("Deck size: " + str(len(self.deck.deck)))
    print("Discard size: " + str(len(self.deck.used_pile)))
    print("")

    t = self.deck.deck + self.deck.used_pile
    for p in self.players:
      t += p.hand
      t += p.money
      for s in p.sets:
        t += s.properties

    all_properties = []
    all_properties_id = []
    money = [0, 0]
    action = [0, 0]
    propertyy = [0, 0]
    rent = [0, 0]

    for c in ALL_CARDS:
      if c == [] or c.id == HOTEL or c.id == HOUSE:
        continue
      if isinstance(c, MoneyCard):
        money[1] += 1
      if isinstance(c, RentCard):
        rent[1] += 1
      if isinstance(c, ActionCard):
        action[1] += 1
      if isinstance(c, PropertyCard):
        all_properties.append(c)
        all_properties_id.append(c.id)
        propertyy[1] += 1

    for c in t:
      if c == [] or c.id == HOTEL or c.id == HOUSE:
        continue
      if isinstance(c, MoneyCard):
        money[0] += 1
      if isinstance(c, RentCard):
        rent[0] += 1
      if isinstance(c, ActionCard):
        action[0] += 1
      if isinstance(c, PropertyCard):
        all_properties.append(c)
        all_properties_id.append(c.id)
        propertyy[0] += 1

    print("money", money, "property", propertyy, "rent", rent, "action", action)

class EndGameResult:
  def __init__(self, ended, draw = None, player = None):
    self.ended = ended
    self.draw = draw
    self.player = player
