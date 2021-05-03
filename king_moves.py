import player_turn, valid_moves

def k_moves(moves,r,c): #is a loop more efficient 
	counter = 1
	get_king_moves(moves,r,c,(r),(c + counter))
	get_king_moves(moves,r,c,(r + counter), (c))
	get_king_moves(moves,r,c,(r), (c- counter))
	get_king_moves(moves,r,c,(r - counter), (c))
	get_king_moves(moves,r,c,(r+counter),(c+counter))
	get_king_moves(moves,r,c,(r-counter),(c-counter))
	get_king_moves(moves,r,c,(r+counter),(c-counter))
	get_king_moves(moves,r,c,(r-counter),(c+counter))
	return moves

def get_king_moves(moves,r,c,x,y):
	if (0 <= x <= 7) and (0 <= y <= 7):
		temp_board = player_turn.board.copy()
		if player_turn.board[r][c] == 6:
			temp_board[x][y] = 6
			temp_board[r][c] = 0
		elif player_turn.board[r][c] ==12:
			temp_board[x][y] =12
			temp_board[r][c] = 0
		checks, pins, king_row, king_col = valid_moves.get_valid_moves(temp_board,x,y)
		if (len(checks) == 0) and  (player_turn.board[r][c] == 6) and (player_turn.white_to_move is True):
			if player_turn.board[x][y] not in player_turn.white_pieces:
				moves.append([(r,c),(x,y)])
			else:
				pass
		else:
			pass
		if (len(checks) == 0) and (player_turn.board[r][c] == 12) and (player_turn.white_to_move is False):
			if player_turn.board[x][y] not in player_turn.black_pieces:
				moves.append([(r,c),(x,y)])
			else:
				pass
		else:
			pass
	return moves