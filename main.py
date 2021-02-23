import numpy as np 


chessBoard = np.array([[0 for x in range(8)] for y in range(8)] )

def pawn_moves(row=3, col=3): #add take functionality
	possible_moves = []

	possible_moves.append([row+1,col]) #if black 
	possible_moves.append([row+2,col])

	# possible_moves.append([row-1,col]) if white
	# possible_moves.append([row-2,col])

	return possible_moves

def knight_moves(row = 0, col = 1): 
	x = 2
	y = 1

	possible_moves=	[[row+x, col-y],
	[row-y, col+x],
	[row-x, col-y],
	[row+x, col+y],
	[row+y, col+x],
	[row-y, col-x],
	[row+y,col-x],
	[row-x,col+y]]

	possible_moves = [i for i in possible_moves if i[0] >=0 and i[0] <= 7 and i[1] >=0 and i[1] <= 7 ]

	return  possible_moves 

def bishop_moves(row = 7, col = 2): 

	#max it can move is 7
	possible_moves=[]
	counter = 1

	while counter <8:
		
		row_pos = row+counter 
		col_pos= col+counter
		row_neg = row-counter
		col_neg = col-counter

		possible_moves.append([row+counter,col+counter])
		possible_moves.append([row-counter,col-counter])
		possible_moves.append([row+counter,col-counter])
		possible_moves.append([row-counter,col+counter])
		counter= counter + 1
	
	possible_moves = [i for i in possible_moves if i[0] >=0 and i[0] <= 7 and i[1] >=0 and i[1] <= 7 ]
	
	return possible_moves
		
def rook_moves(row = 3, col =3):
	possible_moves = []

	counter = 1
	while counter < 8:

		possible_moves.append([row,col + counter])
		possible_moves.append([row + counter, col])
		possible_moves.append([row, col - counter])
		possible_moves.append([row - counter, col])

		counter= counter + 1

	possible_moves = [i for i in possible_moves if i[0] >=0 and i[0] <= 7 and i[1] >=0 and i[1] <= 7 ]

	return possible_moves

def queen_moves(row=3,col=3):
	possible_moves = []

	counter = 1
	while counter < 8:

		possible_moves.append([row,col + counter])
		possible_moves.append([row + counter, col])
		possible_moves.append([row, col - counter])
		possible_moves.append([row - counter, col])
		possible_moves.append([row+counter,col+counter])
		possible_moves.append([row-counter,col-counter])
		possible_moves.append([row+counter,col-counter])
		possible_moves.append([row-counter,col+counter])
		counter= counter + 1

	possible_moves = [i for i in possible_moves if i[0] >=0 and i[0] <= 7 and i[1] >=0 and i[1] <= 7 ]

	return possible_moves

def king_moves(row=3,col=3):
	possible_moves=[]

	counter = 1

	possible_moves.append([row,col + counter])
	possible_moves.append([row + counter, col])
	possible_moves.append([row, col - counter])
	possible_moves.append([row - counter, col])
	possible_moves.append([row+counter,col+counter])
	possible_moves.append([row-counter,col-counter])
	possible_moves.append([row+counter,col-counter])
	possible_moves.append([row-counter,col+counter])

	possible_moves = [i for i in possible_moves if i[0] >=0 and i[0] <= 7 and i[1] >=0 and i[1] <= 7 ]

	return possible_moves

possible_moves = pawn_moves()
print(possible_moves)
