import numpy as np 
import pygame as p
import pawn_moves,knight_moves,bishop_moves,rook_moves,move_finder
import player_turn

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT/DIMENSION
en_p = []

# TO DO
# draws arent accounted for 

def load_images():
	temp = {}
	pieces = ['wP','wN','wB','wR','wQ','wK','bP','bN','bB','bR','bQ','bK']
	for piece in pieces:
		temp[piece] = p.image.load('images/' + piece + '.png')
	ini_list = range(1, 13)
	images = dict(zip(ini_list, list(temp.values())))
	return images

def read_fen(): 
	board = np.array([[0 for x in range(8)] for y in range(8)])
	fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

	d = {'P': 1,'N' : 2,'B' : 3,'R' : 4,'Q' : 5,'K' : 6,'p' : 7,'n' : 8,'b' : 9,'r' : 10,'q' : 11,'k' : 12}

	rank = 0 #row
	file = 0 #column

	for char in fen:
		if char.isdigit() is True:
			file += int(char)
		elif char == '/':
			rank += 1 
			file = 0
		elif char in d.keys():
			board[rank][file] = d.get(char)
			file += 1
		elif char == ' ':
			if (fen[fen.index(char) + 1]) == 'w':
					player_turn.white_to_move = True 
					break
			elif (fen[fen.index(char)+1])== 'b':
					player_turn.white_to_move = False 
					break
	return board, player_turn.white_to_move

def main():
	p.init()
	window = p.display.set_mode((WIDTH, HEIGHT))
	clock = p.time.Clock()
	window.fill((255, 255, 255))
	chess_board , player_turn.white_to_move = read_fen()
	en_Passant = []
	valid_moves, checks = resolve_checks(chess_board,en_Passant)
	move_made = False #dont generate moves untill gamestate changes 
	images = load_images()
	running = True
	sq_clicked = ()
	sqs_clicked = []
	move_log = []
	player_one = True #human is true, ai is false, for the white pieces
	player_two = False #same as above but for black pieces. (could change to integer for different strength ai)
	
	while running:
		human_turn = (player_turn.white_to_move is True and player_one) or (not player_turn.white_to_move and player_two)
		for e in p.event.get():
			if e.type == p.QUIT:
				running = False
			elif e.type == p.MOUSEBUTTONDOWN:
				if human_turn:
					location = p.mouse.get_pos()
					col = location[0]//SQ_SIZE 
					row = location[1]//SQ_SIZE
					sq_clicked = (row,col)
					sqs_clicked.append(sq_clicked)
					if len(sqs_clicked) == 2:
						if sqs_clicked[0] == sqs_clicked[1]: #if user clicks same square
							pass
						else:
							if (player_turn.white_to_move is True and chess_board[int(sqs_clicked[0][0])][int(sqs_clicked[0][1])] in player_turn.white_pieces) or (player_turn.white_to_move is False and 
								chess_board[int(sqs_clicked[0][0])][int(sqs_clicked[0][1])] in player_turn.black_pieces): #correct pieces are moved
								for item in valid_moves:
									if item[0] == (int(sqs_clicked[0][0]),int(sqs_clicked[0][1])) and item[1] == (int(sqs_clicked[1][0]),int(sqs_clicked[1][1])):
										chess_board, enPassant = move_piece(sqs_clicked[0], sqs_clicked[1], chess_board,en_Passant)
										move_made = True
										player_turn.white_to_move =  not player_turn.white_to_move
										print('Whites Move') if player_turn.white_to_move is True else print('Blacks Move')
										move_log.append(item)
										print(move_log)
										break #added so king didnt get two moves when breaking a check
									else: 
										pass
								display_image(images, window, chess_board)
							else:
								pass
						sq_clicked = ()
						sqs_clicked = []
					else:
						pass

		if not human_turn:
			ai_move = move_finder.find_random_move(valid_moves)
			# ai_move = move_finder.find_best_move(chess_board, valid_moves)
			chess_board, enPassant = move_piece(ai_move[0], ai_move[1], chess_board,en_Passant)
			move_made = True
			player_turn.white_to_move =  not player_turn.white_to_move
			move_log.append(ai_move)


		if move_made:
			valid_moves,checks = resolve_checks(chess_board,enPassant)
			valid_moves = castling(valid_moves,move_log,chess_board,checks)
#			print(valid_moves)
			if len(valid_moves) == 0 : 
				if len(checks) != 0:
					print('Checkmate')
					if player_turn.white_to_move is False: 
						print('White Wins')
					else:
						print('Black Wins')
					running = False
				else:
					print('Stalemate')
					running = False
			else:
				pass
		draw_board(window)
		highlight_squares(window,chess_board, valid_moves, sq_clicked)
		display_image(images,window,chess_board)
		clock.tick(15)
		p.display.flip()	
	return

def highlight_squares(window,board, valid_moves, sq_clicked):
	if sq_clicked != ():
		r,c = sq_clicked
		r,c = int(r),int(c)
		if (board[r][c] in player_turn.white_pieces and player_turn.white_to_move is True) or (board[r][c] in player_turn.black_pieces and player_turn.white_to_move is False):
				s = p.Surface((SQ_SIZE,SQ_SIZE))
				s.set_alpha(100)
				s.fill(p.Color('yellow'))
				window.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
				s.fill(p.Color('red'))
				for move in valid_moves:
					if (move[0][0] == r) and (move[0][1] == c):
						window.blit(s,(move[1][1]*SQ_SIZE,move[1][0]*SQ_SIZE))
	return 

def castling(moves,move_log,board,checks):
#	global player_turn.white_to_move
	white_left = False
	white_right = False
	black_left = True
	black_right = True
	for move in move_log:
		if player_turn.white_to_move is True:
			if move[0] == (7,4):
				return moves
			elif len(checks) != 0:
				return moves
			else: 
				for move in move_log:
					if move[0] == (7,0):
					 	white_left = True
					 	break
					else:
						pass
					if move[0] ==(7,7):
						white_right = True
						break
					else:
						pass
		if player_turn.white_to_move is False:
			if move[0] == (0,4):
				return moves
			elif len(checks) != 0:
				return moves
			else: 
				for move in move_log:
					if move[0] == (0,0):
					 	black_left = True
					 	break
					else:
						pass
					if move[0] ==(0,7):
						black_right = True
						break
					else:
						pass

	if white_left is False and board[7][1] ==0 and board[7][2] ==0 and board[7][3] ==0:
		checks, pins, king_row, king_col = get_valid_moves(board,7,1)
		checks1,pins, king_row, king_col = get_valid_moves(board,7,2)
		if len(checks) == 0 and len(checks1) == 0:
				 moves.append([(7,4),(7,2)])
	elif white_right is False and board[7][5] == 0 and board[7][6] ==0:
		checks2, pins, king_row, king_col = get_valid_moves(board,7,5)
		checks3,pins, king_row, king_col = get_valid_moves(board,7,6)
		if len(checks2) == 0 and len(checks3) == 0:
			moves.append([(7,4),(7,6)])

	if black_left is False and board[0][1] ==0 and board[0][2] ==0 and board[0][3] ==0:
		checks, pins, king_row, king_col = get_valid_moves(board,0,1)
		checks1,pins, king_row, king_col = get_valid_moves(board,0,2)
		if len(checks) == 0 and len(checks1) == 0:
				 moves.append([(0,4),(0,2)])
	elif white_right is False and board[0][5] == 0 and board[0][6] ==0:
		checks2, pins, king_row, king_col = get_valid_moves(board,0,5)
		checks3,pins, king_row, king_col = get_valid_moves(board,0,6)
		if len(checks2) == 0 and len(checks3) == 0:
			moves.append([(0,4),(0,6)])

	return moves

def get_all_moves(board,pins,en_Passant): 
	counter = 0
	moves = []
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == 1 or board[i][j] == 7: #get all pawn moves
				moves = pawn_moves.p_moves(moves, i,j,board,pins,en_Passant)
				pass
			elif board[i][j] == 2 or board[i][j] == 8: #get all knight moves 
				moves = knight_moves.k_moves(moves, i,j,board,pins)
				pass
			elif board[i][j] == 3 or board[i][j] == 9: #get all bishop moves 
				moves = bishop_moves.b_moves(moves,i,j,board,pins)
				pass
			elif board[i][j] == 4 or board[i][j] == 10: #get all rook moves 
				moves = rook_moves.r_moves(moves,i,j,board,pins)
				pass
			elif board[i][j] == 5 or board[i][j] == 11: #get all queen moves 
				moves = rook_moves.r_moves(moves,i,j,board,pins)
				moves = bishop_moves.b_moves(moves,i,j,board,pins)
				pass
			elif board[i][j] == 6 or board[i][j] == 12: #get all king moves 
				moves = king_moves(moves,i,j,board)
				pass
	return moves

def get_king_location(board):
	for i in range(len(board)):
		for j in range(len(board[i])):
			if (player_turn.white_to_move is True) and (board[i][j] == 6):
				king_row = i
				king_col = j
			elif (player_turn.white_to_move is False) and (board[i][j] == 12): #get all king moves 
				king_row = i
				king_col = j
	return king_row,king_col

def get_valid_moves(board, x=100,y=0): 
	directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)) #up,down,left,right , four diagonals
	checks = []
	pins = []
	if x == 100:
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
					if board[row][column] == 0:
						pass
					elif (player_turn.white_to_move == False and board[row][column] in player_turn.black_pieces) or (player_turn.white_to_move == True and board[row][column] in player_turn.white_pieces): 
						ally_counter = ally_counter + 1
						if possible_pin == ():
							possible_pin = (row,column,direction[0],direction[1])
						else:
							break
					elif (player_turn.white_to_move == False and board[row][column] in player_turn.white_pieces) or (player_turn.white_to_move == True and board[row][column] in player_turn.black_pieces): 
						enemy_counter = enemy_counter + 1 
						if (i == 1) and ((board[row][column] == 1 and (6<=j<=7)) or (board[row][column] == 7 and (4<=j<=5))):
							if ally_counter == 0: # add conditions in which pawn is checking king
								checks.append((row,column,direction[0],direction[1]))
							elif ally_counter == 1:
								break
						elif (4<=j<=7) and (board[row][column] == 3 or board[row][column] == 9):
							if ally_counter == 0:
								checks.append((row,column,direction[0],direction[1]))
							elif ally_counter == 1:
								pins.append(possible_pin)
						elif (0<=j<=3) and (board[row][column] == 4 or board[row][column] == 10):
							if ally_counter == 0:
								checks.append((row,column,direction[0],direction[1]))
							elif ally_counter == 1:
								pins.append(possible_pin)
						elif board[row][column] == 5 or board[row][column] == 11:
							if ally_counter == 0:
								checks.append((row,column,direction[0],direction[1]))
							elif ally_counter == 1:
								pins.append(possible_pin)
						elif (i ==1) and (board[row][column] == 6 or board[row][column] == 12): 
							if ally_counter == 0: # add conditions in which pawn is checking king
								checks.append((row,column,direction[0],direction[1]))
							elif ally_counter == 1:
								break
						else:
							break
			else:
				break
	knight_moves = [(-2,-1),(-1,-2),(-1,2),(-2,1),(2,-1),(1,-2),(1,2),(2,1)] #seperate loop needed for knight moves
	for move in knight_moves:
		if 0<= king_row+move[0] <=7 and 0<= king_col+move[1] <=7:
			if board[king_row][king_col] == 12 and board[king_row+move[0]][king_col+move[1]] == 2: # and player_turn.white_to_move?
				checks.append((king_row+move[0],king_col+move[1]))
			elif board[king_row][king_col] == 6 and board[king_row+move[0]][king_col+move[1]] == 8:
				checks.append((king_row+move[0],king_col+move[1]))
	return checks,pins,king_row,king_col


def resolve_checks(board,en_Passant): 
	checks, pins,king_row,king_col = get_valid_moves(board)
	moves = get_all_moves(board,pins,en_Passant) 
	valid_squares = []
	if len(checks) == 0:
		return moves,checks  #minus pins which are calculated in individual move functions eg pawn_moves 
	elif len(checks) == 1:
		check = checks[0]
		check_row = check[0]
		check_col = check[1]

		if board[check_row][check_col] ==2 or board[check_row][check_col] ==8:#if knight - must take or move (no block)
			valid_squares = [check_row,check_col]
		else:
			for i in range(1,8):
				valid_square = (king_row + check[2]*i, king_col + check[3]*i) #search in direction of check until attacking piece is reached 
				valid_squares.append(valid_square)
				if valid_square == (check_row,check_col):
					break
		moves = [move for move in moves if move[1] in valid_squares]  
		moves = king_moves(moves,king_row,king_col,board)		
	elif len(checks) == 2:
		moves = king_moves(moves,king_row,king_col,board) 	
	return moves, checks

def move_piece(old_square, new_square, board,en_Passant):
	global en_p
	old_row,old_col,new_row,new_col = old_square[0], old_square[1],new_square[0],new_square[1]
	old_row, old_col,new_row,new_col  = int(old_row), int(old_col),int(new_row),int(new_col)
	board = en_passant_take(old_row, old_col,new_row, new_col,en_p,board)
	en_Passant = check_en_Passant(old_row, old_col,new_row,new_col,board) 
	board = check_castle(old_row,old_col,new_row,new_col,board)
	board = check_promotion(old_row,old_col,new_row,new_col,board)
	
	en_p = en_Passant

	temp = board[old_row:old_row+1, old_col:old_col+1]
	if temp == 0: 
		pass
	else:
		temp = int(temp)
		board[new_row:new_row+1, new_col:new_col+1] = temp 
		board[old_row:old_row+1, old_col:old_col+1] = 0
	return board, en_Passant

def check_en_Passant(old_row, old_col,new_row,new_col,board): #white to move logic here is null and void 
	en_passant = []
	if player_turn.white_to_move is False and board[old_row][old_col] == 7:
		if old_row == 1 and new_row == 3:
			en_passant.append((new_row, new_col))
		else:
			pass
	elif player_turn.white_to_move is True and board[old_row][old_col] == 1:
		if old_row == 6 and new_row == 4:
			en_passant.append((new_row, new_col))
		else:
			pass
	else:
		pass 
	return en_passant 

def en_passant_take(old_r,old_c ,r,c,en_Passant,board):
	if (player_turn.white_to_move is True) and (len(en_Passant)!= 0) and (r - old_r == -1) and (((old_r,old_c-1) in en_Passant) or ((old_r,old_c+1) in en_Passant)) and (old_c - c == -1 or old_c - c == 1):
		board[en_Passant[0][0]][en_Passant[0][1]] = 0
	elif (player_turn.white_to_move is False) and (len(en_Passant)!= 0) and (r - old_r == 1) and (((old_r,old_c-1) in en_Passant) or ((old_r,old_c+1) in en_Passant)) and (old_c - c == -1 or old_c - c == 1):
		board[en_Passant[0][0]][en_Passant[0][1]] = 0

	return board

def check_promotion(old_r,old_c,r,c,board):
	if player_turn.white_to_move is True and board[old_r][old_c] == 1 and r == 0:
		board[old_r][old_c] = 5
	elif player_turn.white_to_move is False and board[old_r][old_c] == 7 and r == 7:
		board[old_r][old_c] = 11
	else:
		pass
	return board

def check_castle(old_r,old_c,r,c,board):
	if old_r == 7 and old_c == 4:
		if r == 7 and c == 2:
			board[7][0] = 0
			board[7][3] = 4
		elif r == 7 and c == 6:
			board[7][7] = 0
			board[7][5] = 4
		else:
			pass
	elif old_r ==0 and old_c ==4:
		if r == 0 and c == 2:
			board[0][0] = 0
			board[0][3] = 10
		elif r == 0 and c == 6:
			board[0][7] = 0
			board[0][5] = 10
		else:
			pass
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

# def animate_move(move,window,board,clock): #to finish later
# 	coords = []
# 	dr = move[1][0] - move[0][0] #row distance (end row - end column)
# 	dc = move[1][1] - move[0][1] 
# 	frames_per_square = 20
# 	frame_count = abs(dr) + abs(dc)* frames_per_square

# 	for frame in range(frame_count +1):
# 		r,c = (move[0][0]+ dr*frame/frames_count,move[0][1]+  dc*frame/frame_count)
# 		draw_board(window)




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
		temp_board = board.copy()
		if board[r][c] == 6:
			temp_board[x][y] = 6
			temp_board[r][c] = 0
		elif board[r][c] ==12:
			temp_board[x][y] =12
			temp_board[r][c] = 0
		checks, pins, king_row, king_col = get_valid_moves(temp_board,x,y)
		if (len(checks) == 0) and  (board[r][c] == 6) and (player_turn.white_to_move is True):
			if board[x][y] not in player_turn.white_pieces:
				moves.append([(r,c),(x,y)])
			else:
				pass
		else:
			pass
		if (len(checks) == 0) and (board[r][c] == 12) and (player_turn.white_to_move is False):
			if board[x][y] not in player_turn.black_pieces:
				moves.append([(r,c),(x,y)])
			else:
				pass
		else:
			pass
	return moves

if __name__ == "__main__" :
	main()
