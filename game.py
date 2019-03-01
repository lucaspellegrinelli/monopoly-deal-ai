import cardsdb
import player
import random
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

class Deck:
  def __init__(self):
    self.deck = random.shuffle(list(ALL_CARDS))
    self.used_pile = []

  def draw(self):
    if len(self.deck) == 0:
      self.deck = random.shuffle(list(self.used_pile))
      self.used_pile = []

    return self.deck.pop(0)

  def getCards(self, number):
    cards = []
    for i in range(number):
      cards.append(self.draw())
    return cards


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
        if property.numberOfProperties() >= property.numberToComplete():
          completed_count += 1
      if completed_count >= self.completedSetsToWin:
        return True
    return False

  def getPossibleMoves(self, player):
    return []

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
