import numpy as np 
import pygame as p
import player_turn, pawn_moves,knight_moves,bishop_moves,rook_moves,king_moves,valid_moves,castle,piece_mover,move_finder

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT/DIMENSION

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
	player_turn.read_fen(player_turn.board)
	v_moves, checks = resolve_checks()
	move_made = False #dont generate moves untill gamestate changes 
	images = load_images()
	running = True
	sq_clicked = ()
	sqs_clicked = []
	move_log = []
	player_one = True #human is true, ai is false, for the white pieces
	player_two = True #same as above but for black pieces. (could change to integer for different strength ai)
	
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
							if (player_turn.white_to_move is True and player_turn.board[int(sqs_clicked[0][0])][int(sqs_clicked[0][1])] in player_turn.white_pieces) or (player_turn.white_to_move is False and 
								player_turn.board[int(sqs_clicked[0][0])][int(sqs_clicked[0][1])] in player_turn.black_pieces): #correct pieces are moved
								for item in v_moves:
									if item[0] == (int(sqs_clicked[0][0]),int(sqs_clicked[0][1])) and item[1] == (int(sqs_clicked[1][0]),int(sqs_clicked[1][1])):
										piece_mover.move_piece(sqs_clicked[0], sqs_clicked[1])
										move_made = True
										player_turn.white_to_move =  not player_turn.white_to_move
										print('Whites Move') if player_turn.white_to_move is True else print('Blacks Move')
										move_log.append(item)
										print(move_log)
										break #added so king didnt get two moves when breaking a check
									else: 
										pass
								display_image(images, window)
							else:
								pass
						sq_clicked = ()
						sqs_clicked = []
					else:
						pass
			elif e.type == p.KEYDOWN:
				if e.key == p.K_z:
					undo_move(move_log)

		if not human_turn:
			ai_move = move_finder.find_random_move(v_moves)
			# ai_move = move_finder.find_best_move(chess_board, v_moves)
			piece_mover.move_piece(ai_move[0], ai_move[1], chess_board)
			move_made = True
			player_turn.white_to_move =  not player_turn.white_to_move
			move_log.append(ai_move)


		if move_made:
			v_moves,checks = resolve_checks()
			print(len(v_moves))
			v_moves = castle.castling(v_moves,move_log,checks)
			if len(v_moves) == 0 : 
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
		highlight_squares(window, v_moves, sq_clicked)
		display_image(images,window)
		clock.tick(15)
		p.display.flip()	
	return

def highlight_squares(window, moves, sq_clicked):
	if sq_clicked != ():
		r,c = sq_clicked
		r,c = int(r),int(c)
		if (player_turn.board[r][c] in player_turn.white_pieces and player_turn.white_to_move is True) or (player_turn.board[r][c] in player_turn.black_pieces and player_turn.white_to_move is False):
				s = p.Surface((SQ_SIZE,SQ_SIZE))
				s.set_alpha(100)
				s.fill(p.Color('yellow'))
				window.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
				s.fill(p.Color('red'))
				for move in moves:
					if (move[0][0] == r) and (move[0][1] == c):
						window.blit(s,(move[1][1]*SQ_SIZE,move[1][0]*SQ_SIZE))
	return 

def get_all_moves(pins): 
	counter = 0
	moves = []
	for i in range(len(player_turn.board)):
		for j in range(len(player_turn.board[i])):
			if player_turn.board[i][j] == 1 or player_turn.board[i][j] == 7: #get all pawn moves
				moves = pawn_moves.p_moves(moves, i,j,pins)
				pass
			elif player_turn.board[i][j] == 2 or player_turn.board[i][j] == 8: #get all knight moves 
				moves = knight_moves.n_moves(moves, i,j,pins)
				pass
			elif player_turn.board[i][j] == 3 or player_turn.board[i][j] == 9: #get all bishop moves 
				moves = bishop_moves.b_moves(moves,i,j,pins)
				pass
			elif player_turn.board[i][j] == 4 or player_turn.board[i][j] == 10: #get all rook moves 
				moves = rook_moves.r_moves(moves,i,j,pins)
				pass
			elif player_turn.board[i][j] == 5 or player_turn.board[i][j] == 11: #get all queen moves 
				moves = rook_moves.r_moves(moves,i,j,pins)
				moves = bishop_moves.b_moves(moves,i,j,pins)
				pass
			elif player_turn.board[i][j] == 6 or player_turn.board[i][j] == 12: #get all king moves 
				moves = king_moves.k_moves(moves,i,j)
				pass
	return moves

def resolve_checks(): 
	checks, pins,king_row,king_col = valid_moves.get_valid_moves()
	moves = get_all_moves(pins) 
	valid_squares = []
	if len(checks) == 0:
		return moves,checks  #minus pins which are calculated in individual move functions eg pawn_moves 
	elif len(checks) == 1:
		check = checks[0]
		check_row = check[0]
		check_col = check[1]

		if player_turn.board[check_row][check_col] ==2 or player_turn.board[check_row][check_col] ==8:#if knight - must take or move (no block)
			valid_squares = [check_row,check_col]
		else:
			for i in range(1,8):
				valid_square = (king_row + check[2]*i, king_col + check[3]*i) #search in direction of check until attacking piece is reached 
				valid_squares.append(valid_square)
				if valid_square == (check_row,check_col):
					break
		moves = [move for move in moves if move[1] in valid_squares]  
		moves = king_moves.k_moves(moves,king_row,king_col)		
	elif len(checks) == 2:
		moves = king_moves.k_moves(moves,king_row,king_col) 	
	return moves, checks

def undo_move(move_log):
	#replaces curernt gamestate with previous one, note that white_to_move is opposite, 
	if len(move_log) !=0:
		move = move_log.pop()
		square = player_turn.taken_square.pop()
		temp = player_turn.board[move[1][0]][move[1][1]]
		player_turn.board[move[1][0]][move[1][1]] = square
		player_turn.board[move[0][0]][move[0][1]] = temp

		if player_turn.en_passant_bool: #en passant functionality 
			if player_turn.white_to_move:
				print('hi',move[0][0],move[0][1],move[1][0],move[1][1])
				player_turn.board[(move[1][0]) -1][move[1][1]] = 1
				player_turn.en_p.append((move[0][0],move[1][1]))
			else:
				player_turn.board[(move[1][0]) +1][move[1][1]] = 7
				player_turn.en_p.append((move[0][0],move[1][1]))
		player_turn.en_passant_bool = False
		
		if player_turn.white_to_move == False: #castling functioanlity
			if player_turn.white_castle_kingside:
				player_turn.board[7][5] = 0
				player_turn.board[7][7] = 4
				player_turn.white_castle_kingside = False
			elif player_turn.white_castle_queenside:
				player_turn.board[7][3] = 0
				player_turn.board[7][0] = 4
				player_turn.white_castle_queenside = False
		elif player_turn.white_to_move == True:
			if player_turn.black_castle_kingside:
				player_turn.board[0][5] = 0
				player_turn.board[0][7] = 10
				player_turn.black_castle_kingside = False
			elif player_turn.black_castle_queenside:
				player_turn.board[0][3] = 0
				player_turn.board[0][0] = 10
				player_turn.black_castle_queenside = False

		if player_turn.white_to_move == False: #promotion functionality
			if player_turn.white_promotion == True:
				player_turn.board[move[0][0]][move[0][1]] = 1
				player_turn.white_promotion = False
		elif player_turn.white_to_move == True:
			if player_turn.black_promotion == True:
				player_turn.board[move[0][0]][move[0][1]] = 7
				player_turn.black_promotion = False

	# elif len(move_log) == 0:
	# 	print('hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')

		player_turn.white_to_move = not player_turn.white_to_move
	return

def draw_board(window): #some of this should go in main 
	colour1 = (235, 235, 208)
	colour2 = (119, 148, 85)
	colors = [colour1,colour2]
	for i in range(8):
	  for j in range(8):
	    color = colors[((i+j) % 2)]
	    p.draw.rect(window,color,p.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
	
def display_image(images, window):
	for i in range(8):
	      for j in range(8):
	      	piece = player_turn.board[i][j]
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

if __name__ == "__main__" :
	main()
