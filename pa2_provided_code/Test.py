from MancalaGUI import *
player1 = MancalaPlayer(1,Player.MINIMAX, ply=5)
player2 = MancalaPlayer(2,Player.MINIMAX,ply=5)
startGame(player1,player2)
