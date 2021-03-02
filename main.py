import numpy as np 
import pygame as p

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT/DIMENSION

# TO
# integrate board2.py with main 

def main():
	chessBoard = np.array([[0 for x in range(8)] for y in range(8)])
	chessBoard = starting_position(chessBoard)

	print(chessBoard)
	load_images(chessBoard)

	return


def starting_position(chessBoard):
	chessBoard[0, ] = [10,8,9,12,11,9,8,10]
	chessBoard[1] = 7
	chessBoard[-2] = 1
	chessBoard[-1, ] = [4,2,3,6,7,3,2,4]

	return chessBoard

def draw_board(): #some of this should go in main 
	p.init()

	window = p.display.set_mode((WIDTH, HEIGHT))
	clock = p.time.Clock()

	run = True
	while run:
	    clock.tick(60)
	    for event in p.event.get():
	        if event.type == p.QUIT:
	            run = False

	    window.fill((255, 255, 255))

	    colors = [p.Color('white'),p.Color('gray')]
	    for i in range(8):
	      for j in range(8):
	        color = colors[((i+j) % 2)]
	        p.draw.rect(window,color,p.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
	        


	    p.display.flip()

	p.quit()
	exit()


def load_images(chessBoard):
	images = {}
	pieces = ['wP','wN','wB','wR','wQ','wK','bP','bN','bB','bR','bQ','bK']
	for piece in pieces:
		images[piece] = p.image.load('images/' + piece + '.png')



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

# possible_moves = pawn_moves()
# print(possible_moves)


main()
