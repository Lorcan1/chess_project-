import player_turn, valid_moves

def k_moves(moves,r,c,board): #is a loop more efficient 
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
		checks, pins, king_row, king_col = valid_moves.get_valid_moves(temp_board,x,y)
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