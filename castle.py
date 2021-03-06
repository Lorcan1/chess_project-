import player_turn 
import valid_moves

def castling(moves,move_log,checks):
	white_left = False
	white_right = False
	black_left =  False
	black_right = False
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

	if white_left is False and player_turn.board[7][1] ==0 and player_turn.board[7][2] ==0 and player_turn.board[7][3] ==0 and player_turn.board[7][4] == 6 and player_turn.board[7][0] == 4 :
		checks, pins, king_row, king_col = valid_moves.get_valid_moves(player_turn.board,7,2)
		checks1,pins, king_row, king_col = valid_moves.get_valid_moves(player_turn.board,7,3)
		if len(checks) == 0 and len(checks1) == 0:
			moves.append([(7,4),(7,2)])
	if white_right is False and player_turn.board[7][5] == 0 and player_turn.board[7][6] ==0 and player_turn.board[7][4] == 6 and player_turn.board[7][7] == 4:
		checks2, pins, king_row, king_col = valid_moves.get_valid_moves(player_turn.board,7,5)
		checks3,pins, king_row, king_col = valid_moves.get_valid_moves(player_turn.board,7,6)
		if len(checks2) == 0 and len(checks3) == 0:
			moves.append([(7,4),(7,6)])

	if black_left is False and player_turn.board[0][1] ==0 and player_turn.board[0][2] ==0 and player_turn.board[0][3] ==0 and player_turn.board[0][4] == 12 and player_turn.board[0][0] == 10:
		checks4, pins, king_row, king_col = valid_moves.get_valid_moves(player_turn.board,0,2)
		checks5,pins, king_row, king_col = valid_moves.get_valid_moves(player_turn.board,0,3)
		if len(checks4) == 0 and len(checks5) == 0:
				 moves.append([(0,4),(0,2)])
	if black_right is False and player_turn.board[0][5] == 0 and player_turn.board[0][6] ==0 and player_turn.board[0][4] == 12 and player_turn.board[0][7] == 10:
		checks6, pins, king_row, king_col = valid_moves.get_valid_moves(player_turn.board,0,5)
		checks7,pins, king_row, king_col = valid_moves.get_valid_moves(player_turn.board,0,6)
		if len(checks6) == 0 and len(checks7) == 0:
			moves.append([(0,4),(0,6)])

	return moves