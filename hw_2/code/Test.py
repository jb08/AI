# from MancalaGUI import *
# player1 = MancalaPlayer(1,Player.MINIMAX, ply=5)
# player2 = MancalaPlayer(2,Player.MINIMAX,ply=5)
# startGame(player1,player2)

from dmw956 import *
from TicTacToe import *
from MancalaBoard import *

game = MancalaBoard()
p1 = dmw956(1, dmw956.CUSTOM)
p2 = Player(2, Player.ABPRUNE, ply=10)

# game.makeMove(p1, 3)
# game.makeMove(p1, 4)
# game.makeMove(p1, 6)
# game.makeMove(p2, 0)
# game.makeMove(p2, 2)
# game.makeMove(p2, 5)
#game.hostGame(p1,p2)

ABPRUNE_won = 0
Other_won = 0
tie = 0

for i in range(3):
	#print i

	game.reset()
	game.hostGame(p1,p2)

	if game.hasWon(1):
		ABPRUNE_won +=1

	elif game.hasWon(2):
		Other_won +=1

	else:
		tie +=1

print "results:"
print "  CUSTOM won: ", ABPRUNE_won
print "  Other won: ", Other_won
print "  tie: ", tie
