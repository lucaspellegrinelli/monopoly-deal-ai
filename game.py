from cardsdb import *
from player import *
from action import *
import copy
import random

class Game:
  def __init__(self, n_players):
    self.actionsPerTurn = 3
    self.startingHandCount = 5
    self.drawPerTurn = 2
    self.completedSetsToWin = 3

    self.noOptionsCount = 0

    self.deck = Deck(ALL_CARDS)
    self.players = [Player(i, self.deck.getCards(self.startingHandCount)) for i in range(n_players)]

  def run(self):
    curr_player = random.randint(0, len(self.players) - 1)

    while not self.gameEnded():
      print("Player #" + str(curr_player) + " turn\n")
      print("Player drew\n")
      print("Deck size: " + str(len(self.deck.deck)))
      print("Discard size: " + str(len(self.deck.used_pile)))

      # t = self.deck.deck + self.deck.used_pile
      # for p in self.players:
      #   t += p.hand
      #   t += p.money
      #   for s in p.sets:
      #     t += s.properties
      #
      # money = [0, 0]
      # action = [0, 0]
      # propertyy = [0, 0]
      # rent = [0, 0]
      #
      # for c in ALL_CARDS:
      #   if c == [] or c.id == HOTEL or c.id == HOUSE:
      #     continue
      #   if isinstance(c, MoneyCard):
      #     money[1] += 1
      #   if isinstance(c, RentCard):
      #     rent[1] += 1
      #   if isinstance(c, ActionCard):
      #     action[1] += 1
      #   if isinstance(c, PropertyCard):
      #     propertyy[1] += 1
      #
      # for c in t:
      #   if c == [] or c.id == HOTEL or c.id == HOUSE:
      #     continue
      #   if isinstance(c, MoneyCard):
      #     money[0] += 1
      #   if isinstance(c, RentCard):
      #     rent[0] += 1
      #   if isinstance(c, ActionCard):
      #     action[0] += 1
      #   if isinstance(c, PropertyCard):
      #     propertyy[0] += 1
      #
      # print("money", money, "property", propertyy, "rent", rent, "action", action)

      self.players[curr_player].hand += self.deck.getCards(self.drawPerTurn)

      self.players[curr_player].printInfo()

      for action in range(self.actionsPerTurn):
        chosen_action = self.players[curr_player].chooseMove(self, self.actionsPerTurn - action)

        if isinstance(chosen_action, DoNothingAction):
          self.noOptionsCount += 1 if isinstance(chosen_action, DoNothingAction) else 0
        else:
          self.noOptionsCount = 0

        print(chosen_action)
        self.applyAction(chosen_action, self.players[curr_player])

      self.players[curr_player].turnPassing()

      discarded_cards = self.players[curr_player].chooseWhatToDiscard(self)
      random.shuffle(discarded_cards)
      self.deck.deck += discarded_cards

      print("")
      self.players[curr_player].printInfo()

      print("\n------- Turn Passing -------\n")
      curr_player = (curr_player + 1) % len(self.players)

  def getInstance(self, player_id):
    instance = Game(len(self.players))
    instance.deck = copy.deepcopy(self.deck)
    instance.players = copy.deepcopy(self.players)
    instance.noOptionsCount = copy.deepcopy(self.noOptionsCount)

    # The played doesn't have info about cards in opponent hand
    # So I need to blend it with the deck
    cards_in_hand = []
    for p in instance.players:
      if p.id != player_id:
        cards_in_hand.append([p.id, len(p.hand)])
        instance.deck.deck += copy.deepcopy(p.hand)
        p.hand = []

    random.shuffle(instance.deck.deck)
    for p in instance.players:
      for c_in_hand in cards_in_hand:
        if p.id == c_in_hand[0]:
          p.hand += instance.deck.getCards(c_in_hand[1])
          break

    return instance

  def gameEnded(self):
    if self.noOptionsCount >= len(self.players) * 3:
      print("Ended on a Draw")
      return True

    for player in self.players:
      completed_count = 0
      for pSet in player.sets:
        if pSet.isCompleted():
          completed_count += 1
      if completed_count >= self.completedSetsToWin:
        print("Player #" + str(player.id) + " won")
        return True
    return False

  def getTurnPossibleMoves(self, player):
    moves = []
    moves.append(DoNothingAction())

    other_players_id = []
    other_players = []
    for p in self.players:
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
        player.sets.append(pSet)
      else:
        action.propertySet.addProperty(pr)

      # Remove card from hand
      player.hand.remove(action.property)
    elif isinstance(action, AddMoneyAction):
      player.money.append(action.money)
      player.hand.remove(action.money)
    elif isinstance(action, AskMoneyAction):
      payments = []
      for p in self.players:
        if p.id in action.targets:
          if p.willNegate(self):
            print("Player #" + str(p.id) + " negated the effect!")
            for c_hand in p.hand:
              if c_hand.id == JUST_SAY_NO:
                self.deck.used_pile.append(copy.deepcopy(copy.deepcopy(c_hand)))
                p.hand.remove(c_hand)
                break
          else:
            payments += p.choosePayment(self, action.money)

      self.deck.used_pile.append(copy.deepcopy(action.card))
      # Remove card from hand
      player.hand.remove(action.card)
      player.recievePayment(payments)
    elif isinstance(action, DrawCardsAction):
      player.hand += self.deck.getCards(action.quantity)
      self.deck.used_pile.append(copy.deepcopy(action.card))
      # Remove card from hand
      player.hand.remove(action.card)
    elif isinstance(action, AddHouseHotelAction):
      if action.house:
        action.pSet.addHouse()
      else:
        action.pSet.addHotel()

      # Remove card from hand
      player.hand.remove(action.card)
    elif isinstance(action, StealPropertyAction):
      stolen_property = copy.deepcopy(action.property)
      for p in other_players:
        if p.id == action.owner:
          for pSet in p.sets:
            if action.property in pSet.properties:
              pSet.properties.remove(action.property)
              break
          break

      self.deck.used_pile.append(copy.deepcopy(action.card))
      # Remove card from hand
      player.hand.remove(action.card)
      player.recievePayment([stolen_property])
    elif isinstance(action, StealPropertySetAction):
      stolen_set = copy.deepcopy(action.pSet)
      for p in other_players:
        if p.id == action.owner and action.pSet in p.sets:
          p.sets.remove(action.pSet)
          break

      self.deck.used_pile.append(copy.deepcopy(action.card))
      # Remove card from hand
      player.hand.remove(action.card)
      player.recievePayment([stolen_set])
    elif isinstance(action, SwapPropertyAction):
      stolen_property = copy.deepcopy(action.other)
      my_property = copy.deepcopy(action.mine)

      for pSet in player.sets:
        if action.mine in pSet.properties:
          pSet.properties.remove(action.mine)

      for p in other_players:
        if p.id == action.other_id:
          for pSet in p.sets:
            if action.other in pSet.properties:
              pSet.properties.remove(action.other)

          p.recievePayment([my_property])

      self.deck.used_pile.append(copy.deepcopy(action.card))
      # Remove card from hand
      player.hand.remove(action.card)
      player.recievePayment([stolen_property])
    elif isinstance(action, ApplyDoubleRent):
      player.doubleRent = True
      self.deck.used_pile.append(copy.deepcopy(action.card))
      # Remove card from hand
      player.hand.remove(action.card)
