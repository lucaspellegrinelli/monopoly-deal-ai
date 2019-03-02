import random

class Player:
  def __init__(self, id, hand):
    self.id = id
    self.hand = hand
    self.sets = []
    self.money = []

    self.doubleRent = False

  def chooseMove(self, instance, possible_moves, moves_left):
    return possible_moves[random.randint(0, len(possible_moves))]

  def choosePayment(self, instance, how_much):
    return []

  def recievePayment(self, payment):
    # Naive
    for card in payment:
      if isinstance(card, MoneyCard) or isinstance(card, ActionCard) or isinstance(card, RentCard):
        money.append(card)
      else:
        for set in self.sets:
          if set.canAddProperty(card):
            set.addProperty(card)
            break
