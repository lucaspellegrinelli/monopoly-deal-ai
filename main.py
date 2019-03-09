import time

from monopoly.game import Game
from monopoly.bots.random_ai import RandomAI

def timeTest():
  it = 10
  start = time.time()
  for i in range(it):
    game = Game(2, RandomAI())
    result = game.run()
  print((time.time() - start) / it)

if __name__ == '__main__':
  timeTest()
  # game = Game(5, RandomAI())
  # result = game.run()
  #
  # print(" ----------------------------------------- ")
  # if result.draw:
  #   print("\tThe game ended on a draw")
  # else:
  #   print("\tThe winner was Player #" + str(result.player.id))
  # print(" ----------------------------------------- ")
