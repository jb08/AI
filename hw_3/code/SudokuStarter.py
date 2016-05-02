#!/usr/bin/env python
import struct, string, math, copy

class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""
  
    def __init__(self, size, board):
      """the constructor for the SudokuBoard"""
      self.BoardSize = size #the size of the board
      self.CurrentGameBoard= board #the current state of the game board

    def set_value(self, row, col, value):
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""

        #add the value to the appropriate position on the board
        self.CurrentGameBoard[row][col]=value
        #return a new board of the same size with the value added
        return SudokuBoard(self.BoardSize, self.CurrentGameBoard)
                                                                  
                                                                  
    def print_board(self):
        """Prints the current game board. Leaves unassigned spots blank."""
        div = int(math.sqrt(self.BoardSize))
        dash = ""
        space = ""
        line = "+"
        sep = "|"
        for i in range(div):
            dash += "----"
            space += "    "
        for i in range(div):
            line += dash + "+"
            sep += space + "|"
        for i in range(-1, self.BoardSize):
            if i != -1:
                print "|",
                for j in range(self.BoardSize):
                    if self.CurrentGameBoard[i][j] > 9:
                        print self.CurrentGameBoard[i][j],
                    elif self.CurrentGameBoard[i][j] > 0:
                        print "", self.CurrentGameBoard[i][j],
                    else:
                        print "  ",
                    if (j+1 != self.BoardSize):
                        if ((j+1)//div != j/div):
                            print "|",
                        else:
                            print "",
                    else:
                        print "|"
            if ((i+1)//div != i/div):
                print line
            else:
                print sep

def parse_file(filename):
    """Parses a sudoku text file into a BoardSize, and a 2d array which holds
    the value of each cell. Array elements holding a 0 are considered to be
    empty."""

    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val
    
    return board
    
def is_complete(sudoku_board):
    """Takes in a sudoku board and tests to see if it has been filled in
    correctly."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    #check each cell on the board for a 0, or if the value of the cell
    #is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col]==0:
                return False
            for i in range(size):
                if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                    return False
                if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                    return False
            #determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == BoardArray[row][col])
                        and (SquareRow*subsquare + i != row)
                        and (SquareCol*subsquare + j != col)):
                            return False
    return True

def init_board(file_name):
    """Creates a SudokuBoard object initialized with values from a text file"""
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)

def solve(initial_board, forward_checking = False, MRV = False, Degree = False,
    LCV = False):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
	BoardArray = initial_board.CurrentGameBoard

	#Check if complete
	if(is_complete(initial_board)):
		return initial_board
	
	#Forward-check

	#Select an unassigned variable
	empty_squares = []
	if(MRV):
		return initial_board
	else if(Degree):
		return initial_board
	else:
		for i in range(0,initial_board.BoardSize):
			for j in range(0,inital_board.BoardSize):
				if(BoardArray[i][j] == 0):
					empty_squares.append((i,j))
	variable = empty_squares.pop()

	#Select ordering for domain of variable
	domain = []
	if (LCV):
		return initial_board
	else:
		# Create a list of the valid values in the variable's domain
		for i in range(1,initial_board.BoardSize+1):
			if (all_dif(initial_board, variable, i)):
				domain.append(i)

	#Look through values	
	for v in domain:
		updated_board = copy.deepcopy(initial_board)
		updated_board.set_value(variable[0], variable[1], v)
		result = solve(updated_board, forward_checking, MRV, Degree, LCV)
		if(is_complete(result)):
			return result
	#Tried all values for a given variable, no valid solution
    return initial_board




def all_dif(initial_board, variable, value):
	
	BoardArray = initial_board.CurrentGameBoard
	row_c = True
	col_c = True
	square_c = True

	# Checks to see if value is present in variable's row
	for i in range(0,initial_board.BoardSize):
		if (BoardArray[variable[0]][i] == value):
			return False
	# Checks to see if value is present in variable's column
	for i in range(0,initial_board.BoardSize):
		if (Board_Array[i][variable[1]] == value):
			return False
	# Checks to see if value is present in variable's subsquare
	subsquare = int(math.sqrt(size))
	SquareRow = variable[0] // subsquare
    SquareCol = variable[1] // subsquare
	for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == value):
                        return False                       
	return True







