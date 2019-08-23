from monopoly.game import Game
from bots.random_ai import RandomAI

if __name__ == '__main__':
	
	# Creates and runs a game with 5 'RandomAI' bots

	players = [
		{
			"name": "Bot 1",
			"ai": RandomAI()
		},
		{
			"name": "Bot 2",
			"ai": RandomAI()
		},
		{
			"name": "Bot 3",
			"ai": RandomAI()
		},
		{
			"name": "Bot 4",
			"ai": RandomAI()
		},
		{
			"name": "Bot 5",
			"ai": RandomAI()
		},
	]

	game = Game(players)

	result = game.run()

	print(" ----------------------------------------- ")
	if result.draw:
		print("\tThe game ended on a draw")
	else:
		print("\tThe winner was " + str(result.player.name))
	print(" ----------------------------------------- ")
