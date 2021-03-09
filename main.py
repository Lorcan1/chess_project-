import numpy as np 
import pygame as p

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT/DIMENSION
white_pieces = [1,2,3,4,5,6]
black_pieces = [7,8,9,10,11,12]

# TO DO
# castling and en passant 
#move long - see 2 

def load_images():
	temp = {}
	pieces = ['wP','wN','wB','wR','wQ','wK','bP','bN','bB','bR','bQ','bK']
	for piece in pieces:
		temp[piece] = p.image.load('images/' + piece + '.png')

	ini_list = range(1, 13)
	images = dict(zip(ini_list, list(temp.values())))

	return images

def starting_position(chessBoard):
	chessBoard[0,] = [10,8,9,12,11,9,8,10]
	chessBoard[1] = 7
	chessBoard[-2] = 1
	chessBoard[-1,] = [4,2,3,5,6,3,2,4]

	return chessBoard
	
def main():
	p.init()
	window = p.display.set_mode((WIDTH, HEIGHT))
	clock = p.time.Clock()
	window.fill((255, 255, 255))

	chessBoard = np.array([[0 for x in range(8)] for y in range(8)])
	chessBoard = starting_position(chessBoard)
	valid_moves = get_all_moves(chessBoard)
	print('/n')
	print(valid_moves)
	move_made = False #dont generate moves untill gamestate changes 3-25

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
				sq_clicked = (row,col)
				sqs_clicked.append(sq_clicked)
				if len(sqs_clicked) == 2:
					if sqs_clicked[0] == sqs_clicked[1]: #if user clicks same square
						pass
					else:
						x= int(sqs_clicked[0][0])#messy same as first few lines as move piece function 
						y= int(sqs_clicked[0][1])
						int_tuple = (x,y)
						i= int(sqs_clicked[1][0])
						j= int(sqs_clicked[1][1])
						int_tuple2 = (i,j)
						for item in valid_moves:
							if item[0] == int_tuple and item[1] == int_tuple2:
								chessBoard = move_piece(sqs_clicked[0], sqs_clicked[1], chessBoard)
								move_made = True
						display_image(images, window, chessBoard)
					sq_clicked = ()
					sqs_clicked = []
				else:
					pass

		if move_made:
			valid_moves = get_all_moves(chessBoard)
		draw_board(window)
		display_image(images,window,chessBoard)
		clock.tick(15)
		p.display.flip()
	
	return

def get_all_moves(board): 
	counter = 0
	moves = []
	hard_moves = [[(6,4),(4,4)]]
	for i in range(len(board)):
		for j in range(len(board[i])):

			if board[i][j] == 1 or board[i][j] == 7: #get all pawn moves
				moves = pawn_moves(moves, i,j,board)
				pass
			elif board[i][j] == 2 or board[i][j] == 8: #get all knight moves 
				moves = knight_moves(moves, i,j,board)
				pass
			elif board[i][j] == 3 or board[i][j] == 9: #get all bishop moves 
				moves = bishop_moves(moves,i,j,board)
				pass
			elif board[i][j] == 4 or board[i][j] == 10: #get all rook moves 
				moves = rook_moves(moves,i,j,board)
				pass
			elif board[i][j] == 5 or board[i][j] == 11: #get all queen moves 
				moves = queen_moves(moves,i,j,board)
				pass
			elif board[i][j] == 6 or board[i][j] == 12: #get all king moves 
				moves = king_moves(moves,i,j,board)
				pass

	return moves


def move_piece(old_square, new_square, board):
	old_row,old_col,new_row,new_col = old_square[0], old_square[1],new_square[0],new_square[1]
	old_row, old_col,new_row,new_col  = int(old_row), int(old_col),int(new_row),int(new_col)
	temp = board[old_row:old_row+1, old_col:old_col+1]
	if temp == 0: 
		pass
	else:
		temp = int(temp)
		board[new_row:new_row+1, new_col:new_col+1] = temp
		board[old_row:old_row+1, old_col:old_col+1] = 0

	return board



def draw_board(window): #some of this should go in main 
	colour1 = (235, 235, 208)
	colour2 = (119, 148, 85)

	colors = [colour1,colour2]
	for i in range(8):
	  for j in range(8):
	    color = colors[((i+j) % 2)]
	    p.draw.rect(window,color,p.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))

	
def display_image(images, window,chessBoard):
	for i in range(8):
	      for j in range(8):
	      	piece = chessBoard[i][j]
	      	if piece != 0:
		      	window.blit(images[piece], p.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def pawn_moves(moves,r,c,board): #add take functionality
	if board[r][c] == 1 and board[r-1][c] == 0 and r != 0:
		moves.append([(r,c),(r-1,c)]) #if white decrease
		if r == 6 and board[r-2][c] ==0: #if in starting row, can move twice
			moves.append([(r,c),(r-2,c)])
		else:
			pass
	elif r != 7 and board[r][c] == 7 and board[r+1][c] == 0:
		moves.append([(r,c),(r+1,c)]) #if black increase
		if r == 1 and board[r+2][c] == 0:
			moves.append([(r,c),(r+2,c)])
		else:
			pass
	else:
		pass
#takes
	if board[r][c] == 1 and board[r-1][c-1] in black_pieces: #take black
		moves.append([(r,c),(r-1,c-1)])
	else:
		pass
	if board[r][c] == 1 and c != 7 and board[r-1][c+1] in black_pieces:
		moves.append([(r,c),(r-1,c+1)])
	else:
		pass

	if r != 7 and board[r][c] == 7 and board[r+1][c-1] in white_pieces: #take white
		moves.append([(r,c),(r+1,c-1)])
	else:
		pass
	if r != 7 and  board[r][c] == 7 and c != 7 and board[r+1][c+1] in white_pieces:
		moves.append([(r,c),(r+1,c+1)])
	else:
		pass
	
	return moves

def knight_moves(moves,r,c,board): 
	x = 2
	y = 1
	moves.extend([[(r,c),(r+x, c-y)],
	[(r,c),(r-y, c+x)],
	[(r,c),(r-x, c-y)],
	[(r,c),(r+x, c+y)],
	[(r,c),(r+y, c+x)],
	[(r,c),(r-y, c-x)],
	[(r,c),(r+y,c-x)],   
	[(r,c),(r-x,c+y)]])

	moves = [i for i in moves if i[1][0] >=0 and i[1][0] <= 7 and i[1][1] >=0 and i[1][1] <= 7 ]

	for i in moves:
		if board[i[0][0]][i[0][1]] == 2 and board[i[1][0]][i[1][1]] in white_pieces:
				moves.remove(i)
		elif board[i[0][0]][i[0][1]] == 8 and board[i[1][0]][i[1][1]] in black_pieces:
				moves.remove(i)	
		else:
			pass		
			
	return moves 

def get_diagonal_moves(moves,r,c,x,y,board,stopper):
	
	temp_list = [r,c,x,y]

	if stopper and all(i >= 0 and i <=7 for i in temp_list):
		if ((board[r][c] == 3 or board[r][c] == 5) and board[x][y] in white_pieces) or ((board[r][c] == 9 or board[r][c] == 11) and board[x][y] in black_pieces):
			pass
		else:
			moves.append([(r,c),(x,y)])
		if board[x][y] != 0:
			stopper = False

	return moves, stopper

def bishop_moves(moves,r,c,board): #remove() doesnt work because it only removes first instance from list 

	counter = 1
	stopper1 = True
	stopper2 = True
	stopper3 = True
	stopper4 = True

	while counter <8:
		if stopper1:
			moves,stopper1 = get_diagonal_moves(moves,r,c,r+counter,c+counter,board,stopper1)
		if stopper2:
			moves,stopper2 = get_diagonal_moves(moves,r,c,r-counter,c-counter,board,stopper2)
		if stopper3:
			moves,stopper3 = get_diagonal_moves(moves,r,c,r+counter,c-counter,board,stopper3)
		if stopper4:
			moves,stopper4 = get_diagonal_moves(moves,r,c,r-counter,c+counter,board,stopper4)

		counter = counter + 1

	return moves
		
def rook_moves(moves,r,c,board):

	counter = 1
	stopper1 = True
	stopper2 = True
	stopper3 = True
	stopper4 = True

	while counter <8:
		if stopper1:
			moves,stopper1 = get_rook_moves(moves,r,c,r,c+counter,board,stopper1)
		if stopper2:
			moves,stopper2 = get_rook_moves(moves,r,c,r+counter,c,board,stopper2)
		if stopper3:
			moves,stopper3 = get_rook_moves(moves,r,c,r,c-counter,board,stopper3)
		if stopper4:
			moves,stopper4 = get_rook_moves(moves,r,c,r-counter,c,board,stopper4)

		counter = counter + 1

	return moves


def get_rook_moves(moves,r,c,x,y,board,stopper):
	
	temp_list = [r,c,x,y]

	if stopper and all(i >= 0 and i <=7 for i in temp_list):
		if((board[r][c] == 4 or board[r][c] == 5)  and board[x][y] in white_pieces) or ((board[r][c] == 10 or board[r][c] == 11) and board[x][y] in black_pieces):
			pass
		else:
			moves.append([(r,c),(x,y)])
		if board[x][y] != 0:
			stopper = False

	return moves, stopper

def queen_moves(moves,r,c,board):

	counter = 1
	stopper1 = True
	stopper2 = True
	stopper3 = True
	stopper4 = True
	stopper5 = True
	stopper6 = True
	stopper7 = True
	stopper8 = True

	while counter <8:
		if stopper1:
			moves,stopper1 = get_diagonal_moves(moves,r,c,r+counter,c+counter,board,stopper1)
		if stopper2:
			moves,stopper2 = get_diagonal_moves(moves,r,c,r-counter,c-counter,board,stopper2)
		if stopper3:
			moves,stopper3 = get_diagonal_moves(moves,r,c,r+counter,c-counter,board,stopper3)
		if stopper4:
			moves,stopper4 = get_diagonal_moves(moves,r,c,r-counter,c+counter,board,stopper4)
		if stopper5:
			moves,stopper5 = get_rook_moves(moves,r,c,r,c+counter,board,stopper5)
		if stopper6:
			moves,stopper6 = get_rook_moves(moves,r,c,r+counter,c,board,stopper6)
		if stopper7:
			moves,stopper7 = get_rook_moves(moves,r,c,r,c-counter,board,stopper7)
		if stopper8:
			moves,stopper8 = get_rook_moves(moves,r,c,r-counter,c,board,stopper8)

		counter = counter + 1

	return moves

def king_moves(moves,r,c,board):
	counter = 1

	get_king_moves(moves,r,c,(r),(c + counter),board)
	get_king_moves(moves,r,c,(r + counter), (c),board)
	get_king_moves(moves,r,c,(r), (c- counter),board)
	get_king_moves(moves,r,c,(r - counter), (c),board)
	get_king_moves(moves,r,c,(r+counter),(c+counter),board)
	get_king_moves(moves,r,c,(r-counter),(c-counter),board)
	get_king_moves(moves,r,c,(r+counter),(c-counter),board)
	get_king_moves(moves,r,c,(r-counter),(c+counter),board)

	return moves

def get_king_moves(moves,r,c,x,y,board):
	if (0 <= x <= 7) and (0 <= y <= 7):
		if (board[x][y] == 0) or (board[r][c] == 6 and board[x][y] in black_pieces) or (board[r][c] == 12 and board[x][y] in white_pieces):
			moves.append([(r,c),(x,y)])

	return moves

if __name__ == "__main__" :
	main()
