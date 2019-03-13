from monopoly.game import Game
from monopoly.bots.random_ai import RandomAI

from genetic_algorithm import *
from fit_func import *

if __name__ == '__main__':
  game = Game(5, RandomAI())
  result = game.run()

  print(" ----------------------------------------- ")
  if result.draw:
    print("\tThe game ended on a draw")
  else:
    print("\tThe winner was Player #" + str(result.player.id))
  print(" ----------------------------------------- ")
