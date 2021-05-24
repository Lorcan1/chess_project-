import player_turn

def undo_move(move_log):
	#replaces curernt gamestate with previous one, note that white_to_move is opposite, 
	if len(move_log) !=0:
		move = move_log.pop()
		white_promotion = player_turn.white_promotion_list.pop()
		black_promotion = player_turn.black_promotion_list.pop()
		white_en_passant_bool = player_turn.white_en_p_list.pop()
		black_en_passant_bool = player_turn.black_en_p_list.pop()

		square = player_turn.taken_square.pop()
		temp = player_turn.board[move[1][0]][move[1][1]]
		player_turn.board[move[1][0]][move[1][1]] = square
		player_turn.board[move[0][0]][move[0][1]] = temp

		if black_en_passant_bool  : #en passant functionality 
				player_turn.board[(move[1][0]) -1][move[1][1]] = 1
				player_turn.en_p.append((move[0][0],move[1][1]))
		elif white_en_passant_bool:
				player_turn.board[(move[1][0]) +1][move[1][1]] = 7
				player_turn.en_p.append((move[0][0],move[1][1]))
			
		if player_turn.white_to_move == False: #castling functioanlity
			if move[0] == (7,4) and move[1] == (7,6):
				player_turn.board[7][5] = 0
				player_turn.board[7][7] = 4
				# player_turn.white_castle_kingside = False
			elif move[0] == (7,4) and move[1] == (7,2):
				player_turn.board[7][3] = 0
				player_turn.board[7][0] = 4
		elif player_turn.white_to_move == True:
			if move[0] == (0,4) and move[1] == (0,6):
				player_turn.board[0][5] = 0
				player_turn.board[0][7] = 10
			elif move[0] == (0,4) and move[1] == (0,2):
				player_turn.board[0][3] = 0
				player_turn.board[0][0] = 10

 
		if white_promotion: #promotion functionality
			player_turn.board[move[0][0]][move[0][1]] = 1
			player_turn.white_promotion = False
	
		elif black_promotion == True:
			player_turn.board[move[0][0]][move[0][1]] = 7
			player_turn.black_promotion = False

		player_turn.white_to_move = not player_turn.white_to_move
	return