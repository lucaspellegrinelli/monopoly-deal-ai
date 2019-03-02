import cardsdb
import player
import copy

class PropertySet:
  def __init__(self, colors):
    self.properties = []
    self.colors = colors

  def addProperty(self, property):
    if self.color in property.colors and self.numberToComplete() > self.numberOfProperties():
      self.properties.append(property)
    else:
      print("Tried to add property. Blocked.")

  def numberOfProperties(self):
    return len(properties)

  def rentValue(self):
    if self.color == BROWN_PROPERTY:
      return len(self.properties)
    elif self.color == DARK_BLUE_PROPERTY:
      return 3 if len(self.properties) == 1 else 8
    elif self.color == GREEN_PROPERTY:
      return 2 * len(self.properties) if len(self.properties) <= 2 else 7
    elif self.color == LIGHT_BLUE_PROPERTY:
      return len(self.properties)
    elif self.color == ORANGE_PROPERTY:
      return 2 * len(self.properties) - 1
    elif self.color == PINK_PROPERTY:
      return 2 ** (len(self.properties) - 1)
    elif self.color == BLACK_PROPERTY:
      return len(self.properties)
    elif self.color == RED_PROPERTY:
      return len(self.properties) + 1 if len(self.properties) <= 2 else 6
    elif self.color == LIGHT_GREEN_PROPERTY:
      return len(self.properties)
    elif self.color == YELLOW_PROPERTY:
      return 2 * len(self.properties)
    else:
      return -1

  def numberToComplete(self):
    if self.color == BROWN_PROPERTY or self.color == DARK_BLUE_PROPERTY or
       self.color == LIGHT_GREEN_PROPERTY:
      return 2
    elif self.color == GREEN_PROPERTY or self.color == LIGHT_BLUE_PROPERTY or
         self.color == ORANGE_PROPERTY or self.color == PINK_PROPERTY or
         self.color == RED_PROPERTY or self.color == YELLOW_PROPERTY:
      return 3
    elif self.color == BLACK_PROPERTY:
      return 4
    else:
      return -1

  def isCompleted():
    return self.numberToComplete() >= self.numberOfProperties()

class Game:
  def __init__(self, n_players):
    self.actionsPerTurn = 3
    self.startingHandCount = 5
    self.drawPerTurn = 2
    self.completedSetsToWin = 3

    self.deck = Deck()
    self.players = [Player(self.deck.getCards(self.startingHandCount)) for i in range(n_players)]

  def getInstance(self):
    instance = Game(len(self.players))
    instance.deck = copy.deepcopy(self.deck)
    instance.players = copy.deepcopy(self.players)
    return instance

  def gameEnded(self):
    for player in self.players:
      completed_count = 0
      for property in player.properties:
        if property.isCompleted():
          completed_count += 1
      if completed_count >= self.completedSetsToWin:
        return True
    return False

  def getPossibleMoves(self, player):
    moves = []

    for card in player.hand:
      if isinstance(card, PropertyCard):
        moves.append(PlayPropertyAction(card, PropertySet(card.colors)))
        for property in player.properties:
          if not property.isCompleted() and len(set(card.colors).intersection(property.colors)) > 0:
            moves.append(PlayPropertyAction(card, property))
      elif isinstance(card, MoneyCard):
        moves.append(AddMoneyAction(card.value))
      elif isinstance(card, RentCard):
        moves.append(AddMoneyAction(card.value))
        for property in player.properties:
          if len(property.colors) == 1 and (property.colors[0] in card.colors or card.wild):
            moves.append(UseRentAction(card.colors, property.colors[0], card.wild))
      elif isinstance(card, ActionCard):
        moves.append(UseActionCard(card.action))
        moves.append(AddMoneyAction(card.value))

  def applyMove(self, move):
    return False

  def run(self):
    curr_player = random.randint(0, len(self.players))
    while not self.gameEnded():
      curr_player = (curr_player + 1) % len(self.players)
      self.players[curr_player].hand.append(self.deck.getCards(self.drawPerTurn))

      for action in range(self.actionsPerTurn):
        possible_moves = getPossibleMoves(self.players[curr_player])
        chosen_move = self.players[curr_player].chooseMove(self.getInstance(), possible_moves, self.actionsPerTurn - action)
        self.applyMove(chosen_move)
