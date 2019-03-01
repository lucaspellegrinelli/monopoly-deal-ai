import random

class Player:
  def __init__(self, hand):
    self.hand = hand
    self.properties = []
    self.money = []

  def chooseMove(self, instance, possible_moves, moves_left):
    return possible_moves[random.randint(0, len(possible_moves))]
