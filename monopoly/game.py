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
      #print("\n--------- Turn Starting ---------\n")
      player = self.players[player_index]
      #print("Player #" + str(player_index) + " turn\n")
      #print("Deck size: " + str(len(self.deck.deck)))
      #print("Discard size: " + str(len(self.deck.used_pile)) + "\n")
      #self.printCardQtdInfo()

      player.addToHand(self.deck.getCards(self.drawPerTurn))

      #print(player)

      for action in range(self.actionsPerTurn):
        chosen_action = player.chooseMove(self.getInstance(player), self.actionsPerTurn - action)
        #print("[Action] " + str(chosen_action))

        if isinstance(chosen_action, DoNothingAction):
          self.noOptionsCount += 1
        else:
          self.noOptionsCount = 0

        self.applyAction(chosen_action, player)

      game_state = self.getGameState()

      player.turnPassing()
      discarded_cards = player.chooseWhatToDiscard(self.getInstance(player))

      #print(player)

      random.shuffle(discarded_cards)
      self.deck.deck += discarded_cards
      player_index = (player_index + 1) % len(self.players)

    #print(game_state.player)
    return game_state

  def getInstance(self, player):
    instance = Game(len(self.players), self.ai)
    instance.deck = copy.deepcopy(self.deck)
    instance.players = copy.deepcopy(self.players)
    instance.noOptionsCount = self.noOptionsCount

    # The played doesn't have info about cards in opponent hand
    # So I need to blend it with the deck
    cards_in_hand = []
    for p in instance.players:
      if p.id != player.id:
        cards_in_hand.append([p.id, len(p.hand)])
        instance.deck.deck += p.hand
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
    moves = [DoNothingAction(player.id)]

    other_players_id = [p.id for p in self.players if p.id != player.id]
    other_players = [p for p in self.players if p.id != player.id]

    for card in player.hand:
      if isinstance(card, PropertyCard):
        if not card.isRainbow():
          moves.append(PlayPropertyAction(player.id, card, PropertySet(card.colors)))
        for property_set in player.sets:
          if property_set.canAddProperty(card):
            moves.append(PlayPropertyAction(player.id, card, property_set))

      elif isinstance(card, MoneyCard):
        moves.append(AddMoneyAction(player.id, card))

      elif isinstance(card, RentCard):
        moves.append(AddMoneyAction(player.id, card))
        for property_set in player.sets:
          if property_set.isDefined() and property_set.rentValue() > 0:
            if card.wild:
              moves += [AskMoneyAction(player.id, card, property_set.rentValue() * (2 if player.doubleRent else 1), [o_player_id]) for o_player_id in other_players_id]
            elif property_set.colors[0] in card.colors:
              moves.append(AskMoneyAction(player.id, card, property_set.rentValue() * (2 if player.doubleRent else 1), other_players_id))

      elif isinstance(card, ActionCard):
        moves.append(AddMoneyAction(player.id, card))

        if card.id == DEBT_COLLECTOR:
          # Force someone to give you 5M
          for op in other_players_id:
            moves.append(AskMoneyAction(player.id, card, 5, [op]))

        elif card.id == ITS_MY_BIRTHDAY:
          # Get 2M from everyone
          moves.append(AskMoneyAction(player.id, card, 2, other_players_id))

        elif card.id == PASS_GO:
          # Draws 2 cards
          moves.append(DrawCardsAction(player.id, card, 2))

        elif card.id == HOUSE:
          # Increases rent value for completed set
          moves += [AddHouseHotelAction(player.id, card, p_set, True) for p_set in player.sets if p_set.isCompleted() and not p_set.isUtility()]

        elif card.id == HOTEL:
          # Increases rent value for houses
          moves += [AddHouseHotelAction(player.id, card, p_set, False) for p_set in player.sets if p_set.hasHouse]

        elif card.id == SLY_DEAL:
          # Steals a single property from a non completed set
          for op in other_players:
            for p_set in op.sets:
              if not p_set.isCompleted():
                moves += [StealPropertyAction(player.id, card, property, op.id) for property in p_set.properties]

        elif card.id == DEAL_BREAKER:
          # Steals a completed property set
          for op in other_players:
            moves += [StealPropertySetAction(player.id, card, p_set, op.id) for p_set in op.sets if p_set.isCompleted()]

        elif card.id == FORCED_DEAL:
          # Forces swap between one of your properties and someone elses property
          my_properties = []
          other_properties = []
          for my_set in player.sets:
            if not my_set.isCompleted() and my_set.numberOfProperties() > 0:
              my_properties += [p for p in my_set.properties]

          for o_player in other_players:
            for other_set in o_player.sets:
              if not other_set.isCompleted() and other_set.numberOfProperties() > 0:
                other_properties += [[p, o_player.id] for p in other_set.properties]

          for my_p in my_properties:
            moves += [SwapPropertyAction(player.id, card, my_p, other_p[0], other_p[1]) for other_p in other_properties]

        elif card.id == DOUBLE_RENT:
          # Doubles the next rent card played this turn
          moves.append(ApplyDoubleRent(player.copy(), card))

    return moves

  def applyAction(self, action, player):
    other_players_id = [p.id for p in self.players if p.id != player.id]
    other_players = [p for p in self.players if p.id != player.id]

    if isinstance(action, PlayPropertyAction):
      if len(action.property_set.properties) == 0:
        p_set = PropertySet(action.property_set.colors)
        p_set.addProperty(action.property)
        player.addPropertySet(p_set)

      elif player.hasPropertySet(action.property_set):
        player.addToPropertySet(action.property_set, action.property)

      player.removeFromHand(action.property)

    elif isinstance(action, AddMoneyAction):
      player.addToMoneyPile(action.money)
      player.removeFromHand(action.money)

    elif isinstance(action, AskMoneyAction):
      payments = []
      for p in self.players:
        if p.id in action.targets:
          if not p.willNegate(self.getInstance(player), action):
            payments += p.choosePayment(self.getInstance(player), action.money)

      self.deck.addToUsedPile(action.card)

      player.removeFromHand(action.card)
      player.recievePayment(self.getInstance(player), payments)

    elif isinstance(action, DrawCardsAction):
      player.hand += self.deck.getCards(action.quantity)
      self.deck.addToUsedPile(action.card)
      player.removeFromHand(action.card)

    elif isinstance(action, AddHouseHotelAction):
      if action.house:
        action.property_set.addHouse()
      else:
        action.property_set.addHotel()

      player.removeFromHand(action.card)

    elif isinstance(action, StealPropertyAction):
      stolen_property = copy.deepcopy(action.property)

      p = self.getPlayer(action.other_player_id)
      if not p.willNegate(self.getInstance(player), action):
        p.removeGeneralProperty(action.property)
        player.recievePayment(self.getInstance(player), [stolen_property])

      self.deck.addToUsedPile(action.card)
      player.removeFromHand(action.card)

    elif isinstance(action, StealPropertySetAction):
      stolen_set = copy.deepcopy(action.property_set)

      p = self.getPlayer(action.other_player_id)
      if not p.willNegate(self.getInstance(player), action):
        p.removePropertySet(action.property_set)
        player.recievePayment(self.getInstance(player), [stolen_set])

      self.deck.addToUsedPile(action.card)
      player.removeFromHand(action.card)

    elif isinstance(action, SwapPropertyAction):
      stolen_property = copy.deepcopy(action.other_property)
      my_property = copy.deepcopy(action.my_property)

      p = self.getPlayer(action.other_player_id)
      if not p.willNegate(self.getInstance(player), action):
        player.removeGeneralProperty(action.my_property)
        p.removeGeneralProperty(action.other_property)
        p.recievePayment(self.getInstance(player), [my_property])
        player.recievePayment(self.getInstance(player), [stolen_property])

      self.deck.addToUsedPile(action.card)
      player.removeFromHand(action.card)

    elif isinstance(action, ApplyDoubleRent):
      player.doubleRent = True
      self.deck.used_pile.append(action.card)
      player.removeFromHand(action.card)

  def getPlayer(self, player_id):
    for p in self.players:
      if p.id == player_id:
        return p

  def printCardQtdInfo(self):
    t = self.deck.deck + self.deck.used_pile
    for p in self.players:
      t += p.hand
      t += p.money
      for s in p.sets:
        t += s.properties

    info = [[0, 0],[0, 0],[0, 0],[0, 0]]

    for c in ALL_CARDS:
      if c == [] or c.id == HOTEL or c.id == HOUSE:
        continue
      if isinstance(c, MoneyCard):
        info[0][1] += 1
      if isinstance(c, RentCard):
        info[1][1] += 1
      if isinstance(c, ActionCard):
        info[2][1] += 1
      if isinstance(c, PropertyCard):
        info[3][1] += 1

    for c in t:
      if c == [] or c.id == HOTEL or c.id == HOUSE:
        continue
      if isinstance(c, MoneyCard):
        info[0][0] += 1
      if isinstance(c, RentCard):
        info[1][0] += 1
      if isinstance(c, ActionCard):
        info[2][0] += 1
      if isinstance(c, PropertyCard):
        info[3][0] += 1

    print("money", info[0], "property", info[2], "rent", info[1], "action", info[2])

class EndGameResult:
  def __init__(self, ended, draw = None, player = None):
    self.ended = ended
    self.draw = draw
    self.player = player
