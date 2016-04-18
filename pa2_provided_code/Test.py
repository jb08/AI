# from MancalaGUI import *
# player1 = MancalaPlayer(1,Player.MINIMAX, ply=5)
# player2 = MancalaPlayer(2,Player.MINIMAX,ply=5)
# startGame(player1,player2)

from Player import *
from TicTacToe import *

game = TTTBoard()
p1 = Player(1, Player.ABPRUNE, ply=7)
p2 = Player(2, Player.ABPRUNE, ply=7)

# game.makeMove(p1, 3)
# game.makeMove(p1, 4)
# game.makeMove(p1, 6)
# game.makeMove(p2, 0)
# game.makeMove(p2, 2)
# game.makeMove(p2, 5)
game.hostGame(p1,p2)

