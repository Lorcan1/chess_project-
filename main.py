import numpy as np 
import pygame as p

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT/DIMENSION

# TO
# integrate board2.py with main 
def load_images():
	temp = {}
	pieces = ['wP','wN','wB','wR','wQ','wK','bP','bN','bB','bR','bQ','bK']
	for piece in pieces:
		temp[piece] = p.image.load('images/' + piece + '.png')

	ini_list = range(1, 13)
	images = dict(zip(ini_list, list(temp.values())))

	return images
	


def main():
	p.init()
	window = p.display.set_mode((WIDTH, HEIGHT))
	clock = p.time.Clock()
	window.fill((255, 255, 255))

	chessBoard = np.array([[0 for x in range(8)] for y in range(8)])
	chessBoard = starting_position(chessBoard)

	images = load_images()

	running = True

	sq_clicked = ()
	sqs_clicked = []

	while running:
		for e in p.event.get():
			if e.type == p.QUIT:
				running = False
			elif e.type == p.MOUSEBUTTONDOWN:
				location = p.mouse.get_pos()
				col = location[0]//SQ_SIZE
				row = location[1]//SQ_SIZE
				sq_clicked = (col,row)
				sqs_clicked.append(sq_clicked)
				if len(sqs_clicked) == 2:
					if sqs_clicked[0] == sqs_clicked[1]:
						pass
					else:
						new_location = sqs_clicked[1]
						new_col = new_location[0]
						new_row = new_location[1]
						chessBoard = move_piece(sqs_clicked[0], sqs_clicked[1], chessBoard)
						display_image(images, window, chessBoard)
					sq_clicked = ()
					sqs_clicked = []
				else:
					pass
		

		
		draw_board(window)
		display_image(images,window,chessBoard)
		clock.tick(15)
		p.display.flip()
	return

def move_piece(old_square, new_square, board):
	old_col,old_row,new_col,new_row = old_square[0], old_square[1],new_square[0],new_square[1]
	old_col, old_row,new_col,new_row   = int(old_col), int(old_row),int(new_col),int(new_row)
	temp = board[old_row:old_row+1, old_col:old_col+1]
	if temp == 0: 
		pass
	else:
		temp = int(temp)
		board[new_row:new_row+1, new_col:new_col+1] = temp
		board[old_row:old_row+1, old_col:old_col+1] = 0

	return board


def starting_position(chessBoard):
	chessBoard[0,] = [10,8,9,12,11,9,8,10]
	chessBoard[1] = 7
	chessBoard[-2] = 1
	chessBoard[-1,] = [4,2,3,5,6,3,2,4]

	return chessBoard

def draw_board(window): #some of this should go in main 
 
	colour1 = (235, 235, 208)
	colour2 = (119, 148, 85)

	colors = [colour1,colour2]
	for i in range(8):
	  for j in range(8):
	    color = colors[((i+j) % 2)]
	    p.draw.rect(window,color,p.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))

	
def display_image(images, window,chessBoard): #rough outline 

#	window.blit(image,(SQ_SIZE*6,SQ_SIZE*6)) #location of piece
	counter = 0
	for i in range(8):
	      for j in range(8):
	      	piece = chessBoard[i][j]
	      	if piece != 0:
	   #   	counter = counter + 1
		      	window.blit(images[piece], p.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))


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

if __name__ == "__main__" :
	main()
