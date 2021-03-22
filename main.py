import numpy as np 
import pygame as p

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT/DIMENSION
white_pieces = [1,2,3,4,5,6]
black_pieces = [7,8,9,10,11,12]
white_to_move = True

# TO DO
# castling and en passant 
#move log - see 2 
#sometimes after one player moves it gets stuck. (if you click too many times)
	#after player whos turn it isnt tries to take? not limited to this

#getting checks completed for black
#king shoudnt be able to move into checkx

def load_images():
	temp = {}
	pieces = ['wP','wN','wB','wR','wQ','wK','bP','bN','bB','bR','bQ','bK']
	for piece in pieces:
		temp[piece] = p.image.load('images/' + piece + '.png')

	ini_list = range(1, 13)
	images = dict(zip(ini_list, list(temp.values())))
	return images

def starting_position(chess_board):
	chess_board[0,] = [10,8,9,12,11,9,8,10]
	chess_board[1] = 7
	chess_board[-2] = 1
	chess_board[-1,] = [4,2,3,5,6,3,2,4]
	return chess_board
	
def main():
	global white_to_move
	p.init()
	window = p.display.set_mode((WIDTH, HEIGHT))
	clock = p.time.Clock()
	window.fill((255, 255, 255))
	chess_board = np.array([[0 for x in range(8)] for y in range(8)])
	chess_board = starting_position(chess_board)
#	valid_moves = get_all_moves(chess_board)
	valid_moves = resolve_checks(chess_board)

#	print('/n')
#	print(valid_moves)

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
				print(sqs_clicked[0])
				if len(sqs_clicked) == 2:
					if sqs_clicked[0] == sqs_clicked[1]: #if user clicks same square
						pass
					else:
						if (white_to_move is True and chess_board[int(sqs_clicked[0][0])][int(sqs_clicked[0][1])] in white_pieces) or (white_to_move is False and 
							chess_board[int(sqs_clicked[0][0])][int(sqs_clicked[0][1])] in black_pieces):
							for item in valid_moves:
								if item[0] == (int(sqs_clicked[0][0]),int(sqs_clicked[0][1])) and item[1] == (int(sqs_clicked[1][0]),int(sqs_clicked[1][1])):
									chess_board = move_piece(sqs_clicked[0], sqs_clicked[1], chess_board)
									move_made = True
									white_to_move =  not white_to_move
									print('Whites Move') if white_to_move is True else print('Blacks Move')
									# checks,pins = get_valid_moves(chess_board)
									# print(pins)
									# print('heyyyyyyyyyyyyyyyyyy')
									#resolve_checks(chess_board)
							display_image(images, window, chess_board)
						sq_clicked = ()
						sqs_clicked = []
				else:
					pass
		if move_made:
#			valid_moves = get_all_moves(chess_board)
			valid_moves = resolve_checks(chess_board)
		draw_board(window)
		display_image(images,window,chess_board)
		clock.tick(15)
		p.display.flip()	
	return

def get_all_moves(board,pins): 
	counter = 0
	moves = []
	hard_moves = [[(6,4),(4,4)]]
	for i in range(len(board)):
		for j in range(len(board[i])):

			if board[i][j] == 1 or board[i][j] == 7: #get all pawn moves
				moves = pawn_moves(moves, i,j,board,pins)
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
				moves = rook_moves(moves,i,j,board)
				moves = bishop_moves(moves,i,j,board)
				pass
			elif board[i][j] == 6 or board[i][j] == 12: #get all king moves 
				moves = king_moves(moves,i,j,board)
				pass
	return moves

def get_king_location(board):
	for i in range(len(board)):
		for j in range(len(board[i])):
			if white_to_move is True and board[i][j] == 6:
				king_row = i
				king_col = j
			elif white_to_move is False and board[i][j] == 12: #get all king moves 
				king_row = i
				king_col = j
				
	return king_row,king_col

def get_valid_moves(board, x=0,y=0): 
	directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)) #up,down,left,right , four diagonals
	checks = []
	pins = []
	checkmate = False 

	if x == 0:
		king_row,king_col = get_king_location(board)
	else:
		king_row = x
		king_col = y

	for j in range(len(directions)):
		possible_pin = ()
		direction = directions[j]
		row = king_row
		column = king_col
		counter = 1
		ally_counter = 0
		enemy_counter = 0
		for i in range(1,8):
			row = king_row + (direction[0]*i)
			column = king_col + (direction[1]*i)
			if ally_counter <2 and enemy_counter < 1:	
				if (0<=row<=7) and (0<=column<=7):
					if white_to_move is False and board[row][column] is 0:
						pass

					elif white_to_move is False and board[row][column] in black_pieces: #if black piece next king ally counter is one 
						ally_counter = ally_counter + 1
						if possible_pin == ():
							possible_pin = (row,column,direction[0],direction[1])
						else:
							break

					elif white_to_move is False and board[row][column] in white_pieces: # if white piece, and 
						enemy_counter = enemy_counter + 1 
					#	print('Theres a check in town')
						if board[row][column] == 1 and (6<=j<=7) and i == 1:
							if ally_counter == 0: # add conditions in which pawn is checking king
								checks.append((row,column,direction[0],direction[1]))
							elif ally_counter == 1:
								break
						elif board[row][column] == 3 and (4<=j<=7):
							if ally_counter == 0:
								checks.append((row,column,direction[0],direction[1]))
							elif ally_counter == 1:
								pins.append(possible_pin)
						elif board[row][column] == 4 and (0<=j<=3):
							if ally_counter == 0:
								checks.append((row,column,direction[0],direction[1]))
							elif ally_counter == 1:
								pins.append(possible_pin)
						elif board[row][column] == 5:
							if ally_counter == 0:
								checks.append((row,column,direction[0],direction[1]))
							elif ally_counter == 1:
								pins.append(possible_pin)
						else:
							break

			else:
				break

	knight_moves = [(-2,-1),(-1,-2),(-1,2),(-2,1),(2,-1),(1,-2),(1,2),(2,1)] #seperate loop needed for knight moves
	for move in knight_moves:
		if 0<= king_row+move[0] <=7 and 0<= king_col+move[1] <=7:
			if white_to_move is False and board[king_row+move[0]][king_col+move[1]] == 2:
				checks.append((king_row+move[0],king_col+move[1]))

	print(checks)
#	print('heyyyyyyyyyyyyyyyy')
	return checks,pins,king_row,king_col


def resolve_checks(board): #checkmate calculated here
	checks, pins,king_row,king_col = get_valid_moves(board)
	moves = get_all_moves(board,pins)
	valid_squares = []

	if len(checks) == 0:
		return moves #minus pins 
	elif len(checks) == 1:
		check = checks[0]
		check_row = check[0]
		check_col = check[1]

		# if board[check_row][check_col] == 1: #capture pawn 
		# 	moves = []
		# 	k_moves = king_moves(moves,king_row,king_col,board)
		# 	return k_moves
		if board[check_row][check_col] ==2:#if knight - must take or move (no block)
			valid_squares = [check_row,check_col]
		else:
			for i in range(1,8):
			#	print('hi')
				valid_square = (king_row + check[2]*i, king_col + check[3]*i) #search in direction of check until attacking piece is reached 
				valid_squares.append(valid_square)
			#	print(valid_squares)
				if valid_square == (check_row,check_col):
					break
		moves = [move for move in moves if move[1] in valid_squares]
		moves = king_moves(moves,king_row,king_col,board)			

	elif len(checks) == 2:
		moves = king_moves(moves,king_row,king_col,board) 
		
	return moves
	#PINS
	#cant move pinned piece, out of pin, can move up and down pin 

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
	
def display_image(images, window,chess_board):
	for i in range(8):
	      for j in range(8):
	      	piece = chess_board[i][j]
	      	if piece != 0:
		      	window.blit(images[piece], p.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def pawn_moves(moves,r,c,board,pins): #add take functionality

 #if pawn is pinned, pawnPinned = True 
 #if true, can only move in direction of pin and cant take 

	if white_to_move is True and board[r][c] == 1 and board[r-1][c] == 0 and r != 0:
		moves.append([(r,c),(r-1,c)]) #if white decrease
		if r == 6 and board[r-2][c] ==0: #if in starting row, can move twice
			moves.append([(r,c),(r-2,c)])
		else:
			pass
	elif white_to_move is False and  r != 7 and board[r][c] == 7 and board[r+1][c] == 0:
		moves.append([(r,c),(r+1,c)]) #if black increase
		if r == 1 and board[r+2][c] == 0:
			moves.append([(r,c),(r+2,c)])
		else:
			pass
	else:
		pass
#takes
	if white_to_move is True and board[r][c] == 1 and board[r-1][c-1] in black_pieces: #take black
		moves.append([(r,c),(r-1,c-1)])
	else:
		pass
	if white_to_move is True and board[r][c] == 1 and c != 7 and board[r-1][c+1] in black_pieces:
		moves.append([(r,c),(r-1,c+1)])
	else:
		pass

	if white_to_move is False and  r != 7 and board[r][c] == 7 and board[r+1][c-1] in white_pieces: #take white
		moves.append([(r,c),(r+1,c-1)])
	else:
		pass
	if  white_to_move is False and r != 7 and  board[r][c] == 7 and c != 7 and board[r+1][c+1] in white_pieces:
		moves.append([(r,c),(r+1,c+1)])
	else:
		pass
	return moves

def knight_moves(moves,r,c,board): #could be done in one for loop
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
		if white_to_move is True and board[i[0][0]][i[0][1]] == 2 and board[i[1][0]][i[1][1]] in white_pieces:
				moves.remove(i)
		elif white_to_move is False and  board[i[0][0]][i[0][1]] == 8 and board[i[1][0]][i[1][1]] in black_pieces:
				moves.remove(i)	
		else:
			pass				
	return moves 

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

def get_diagonal_moves(moves,r,c,x,y,board,stopper):	
	temp_list = [r,c,x,y]
	if stopper and all(i >= 0 and i <=7 for i in temp_list):
		if (white_to_move is True) and (board[r][c] == 3 or board[r][c] == 5) and (board[x][y] in white_pieces):
			pass
		elif white_to_move is True:
			moves.append([(r,c),(x,y)])
		else:
			pass
		if (white_to_move is False) and (board[r][c] == 9 or board[r][c] == 11) and (board[x][y] in black_pieces):
			pass
		elif white_to_move is False:
			moves.append([(r,c),(x,y)])
		else:
			pass
		if board[x][y] != 0:
			stopper = False
		
	return moves, stopper
		
def rook_moves(moves,r,c,board):
	counter = 1
	stopper1 = True
	stopper2 = True
	stopper3 = True
	stopper4 = True
	while counter <8:
		if stopper1:
			moves,stopper1 = get_orthogonal_moves(moves,r,c,r,c+counter,board,stopper1)
		if stopper2:
			moves,stopper2 = get_orthogonal_moves(moves,r,c,r+counter,c,board,stopper2)
		if stopper3:
			moves,stopper3 = get_orthogonal_moves(moves,r,c,r,c-counter,board,stopper3)
		if stopper4:
			moves,stopper4 = get_orthogonal_moves(moves,r,c,r-counter,c,board,stopper4)
		counter = counter + 1
	return moves

def get_orthogonal_moves(moves,r,c,x,y,board,stopper):	
	temp_list = [r,c,x,y]
	if stopper and all(i >= 0 and i <=7 for i in temp_list):
		if(white_to_move is True) and (board[r][c] == 4 or board[r][c] == 5) and (board[x][y] in white_pieces):
			pass
		elif white_to_move is True:
			moves.append([(r,c),(x,y)])
		else:
			pass
		if (white_to_move is False) and (board[r][c] == 10 or board[r][c] == 11) and (board[x][y] in black_pieces):
			pass
		elif white_to_move is False:
			moves.append([(r,c),(x,y)])
		else:
			pass
		if board[x][y] != 0:
			stopper = False
	return moves, stopper

def king_moves(moves,r,c,board): #is a loop more efficient 
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
			checks, pins, king_row, king_col = get_valid_moves(board,x,y)
			if len(checks) == 0:
				moves.append([(r,c),(x,y)])
		else:
			pass

	return moves

if __name__ == "__main__" :
	main()
