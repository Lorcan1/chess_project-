import player_turn

def n_moves(moves,r,c,pins): #could be done in one for loop
	if len(pins) == 0:
		piecePinned = False 
	else:
		for pin in pins:
			if(pin[0] == r and pin[1] == c):
				piecePinned = True 
			else:
				piecePinned = False

	if piecePinned is False:
		x = 2
		y = 1
		k_moves = [(r-y, c+x),(r-x, c-y),(r+x, c+y),(r+y, c+x),(r-y, c-x),(r+y,c-x),(r-x,c+y),(r+x,c-y) ]
		for x in k_moves:
			moves = knight_mover(moves,r,c,x[0],x[1])
	return moves

def knight_mover(moves,r,c,x,y):
	temp_list = [r,c,x,y]
	if all(i >= 0 and i <=7 for i in temp_list):
		if (player_turn.board[r][c] == 2) and (player_turn.white_to_move is True):
			if player_turn.board[x][y] not in player_turn.white_pieces:
				moves.append([(r,c),(x,y)])
			else:
				pass
		if (player_turn.board[r][c] == 8) and (player_turn.white_to_move is False):
			if player_turn.board[x][y] not in player_turn.black_pieces:
				moves.append([(r,c),(x,y)])
			else:
				pass
	return moves