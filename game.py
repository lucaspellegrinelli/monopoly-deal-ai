import cardsdb
import player
import copy

class Game:
  def __init__(self, n_players):
    self.actionsPerTurn = 3
    self.startingHandCount = 5
    self.drawPerTurn = 2
    self.completedSetsToWin = 3

    self.deck = Deck()
    self.players = [Player(i, self.deck.getCards(self.startingHandCount)) for i in range(n_players)]

  def getInstance(self):
    instance = Game(len(self.players))
    instance.deck = copy.deepcopy(self.deck)
    instance.players = copy.deepcopy(self.players)
    return instance

  def gameEnded(self):
    for player in self.players:
      completed_count = 0
      for set in player.sets:
        if set.isCompleted():
          completed_count += 1
      if completed_count >= self.completedSetsToWin:
        return True
    return False

  def getPossibleMoves(self, player):
    moves = []
    other_players_id = [p.id if p.id != player.id for p in self.players]
    other_players = [p if p.id != player.id for p in self.players]

    for card in player.hand:
      if isinstance(card, PropertyCard):
        moves.append(PlayPropertyAction(card, PropertySet(card.colors)))
        for set in player.sets:
          if not set.isCompleted() and len(set(card.colors).intersection(set.colors)) > 0:
            moves.append(PlayPropertyAction(card, set))
      elif isinstance(card, MoneyCard):
        moves.append(AddMoneyAction(card.value))
      elif isinstance(card, RentCard):
        moves.append(AddMoneyAction(card.value))
        for set in player.sets:
          if set.isDefined():
            if card.wild:
              moves.append(AskMoney(set.rentValue(), [x]) for x in other_players_id)
            elif property.colors[0] in card.colors:
              moves.append(AskMoney(set.rentValue(), other_players_id))
      elif isinstance(card, ActionCard):
        moves.append(AddMoneyAction(card.value))
        if card.id == DEBT_COLLECTOR:
          # Force someone to give you 5M
          moves.append(AskMoneyAction(5, [x]) for x in other_players)
        elif card.id == ITS_MY_BIRTHDAY:
          # Get 2M from everyone
          moves.append(AskMoneyAction(2, other_players))
        elif card.id == PASS_GO:
          # Draws 2 cards
          moves.append(DrawCardsAction(2))
        elif card.id == HOUSE:
          # Increases rent value for completed set
          for set in player.sets:
            if set.isCompleted() and not set.isUtility():
              moves.append(AddHouseHotelAction(set, True))
        elif card.id == HOTEL:
          # Increases rent value for houses
          for set in player.sets:
            if set.hasHouse:
              moves.append(AddHouseHotelAction(set, False))
        elif card.id == SLY_DEAL:
          # Steals a single property from a non completed set
          for op in other_players:
            for set in op.sets:
              if not set.isCompleted():
                for property in set.properties:
                  moves.append(StealPropertyAction(property, op.id))
        elif card.id == DEAL_BREAKER:
          # Steals a completed property set
          for op in other_players:
            for set in op.sets:
              if set.isCompleted():
                moves.append(StealPropertySetAction(set, op.id))
        elif card.id == FORCED_DEAL:
          # Forces swap between one of your properties and someone elses property
          my_properties = []
          other_properties = []
          for mySet in player.sets:
            if not mySet.isCompleted():
              my_properties.append([p for p in mySet.properties])

          for otherPlayer in other_players:
            for otherSet in otherPlayer.sets:
              if not otherSet.isCompleted():
                other_properties.append([(p, otherPlayer.id) for p in otherSet.properties])

          for myP in my_properties:
            for otherP in other_properties:
              moves.append(SwapPropertyAction(myP, otherP[0], otherP[1]))
        elif card.id == DOUBLE_RENT:
          # Doubles the next rent card played this turn
          moves.append(ApplyDoubleRent())


  def applyAction(self, action, player):
    if isinstance(action, PlayPropertyAction):
      if len(action.propertySet.properties) == 0:
        pSet = PropertySet(action.propertySet.colors)
        pSet.addProperty(action.property)
        player.sets.append(pSet)
      else:
        action.propertySet.addProperty(action.property)
    elif isinstance(action, AddMoneyAction):
      player.money.append(getMoney(action.money))
    elif isinstance(action, AskMoneyAction):
      payments = []
      for p in self.players:
        if p.id in action.targets:
          if p.willNegate():
            p.hand.remove(JUST_SAY_NO)
          else:
            payments.append(p.choosePayment(self.getInstance(), action.money))

      player.recievePayment(payments)
    elif isinstance(action, DrawCardsAction):
      player.hand.append(self.deck.getCards(action.quantity))
    elif isinstance(action, AddHouseHotelAction):
      if action.house:
        action.set.addHouse()
      else:
        action.set.addHotel()
    elif isinstance(action, StealPropertyAction):
      stolen_property = copy.deepcopy(action.property)
      for p in other_players:
        if p.id == action.owner:
          for set in p.sets:
            if action.property in set.properties:
              set.properties.remove(action.property)
              break
          break
      player.recievePayment([stolen_property])
    elif isinstance(action, StealPropertySetAction):
      stolen_set = copy.deepcopy(action.set)
      for p in other_players:
        if p.id == action.owner and action.set in p.sets:
          p.sets.remove(action.set)
          break
      player.recievePayment(stolen_set)
    elif isinstance(action, SwapPropertyAction):
      stolen_property = copy.deepcopy(action.other)
      my_property = copy.deepcopy(action.mine)

      for set in player.sets:
        if action.mine in set.properties:
          set.properties.remove(action.mine)

      for p in other_players:
        if p.id == action.other_id:
          for set in p.sets:
            if action.other in set.properties:
              set.properties.remove(action.other)

          p.recievePayment([my_property])

      player.recievePayment([stolen_property])
    elif isinstance(action, ApplyDoubleRent):
      player.doubleRent = True


  def run(self):
    curr_player = random.randint(0, len(self.players))
    while not self.gameEnded():
      curr_player = (curr_player + 1) % len(self.players)
      self.players[curr_player].hand.append(self.deck.getCards(self.drawPerTurn))

      for action in range(self.actionsPerTurn):
        possible_moves = getPossibleMoves(self.players[curr_player])
        chosen_action = self.players[curr_player].chooseMove(self.getInstance(), possible_moves, self.actionsPerTurn - action)
        self.applyAction(chosen_action, self.players[curr_player])
