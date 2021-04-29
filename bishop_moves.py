import player_turn

def b_moves(moves,r,c,board,pins): #remove() doesnt work because it only removes first instance from list 
	if len(pins) == 0:
		piecePinned = False 
	else:
		for pin in pins:
			if(pin[0] == r and pin[1] == c):
				piecePinned = True 
				d = (pin[2],pin[3])
			else:
				piecePinned = False
	counter = 1
	stopper1 = True
	stopper2 = True
	stopper3 = True
	stopper4 = True
	while counter <8:
		if stopper1 and (piecePinned == False or (d == (1,1) or d ==(-1,-1))):
			moves,stopper1 = get_diagonal_moves(moves,r,c,r+counter,c+counter,board,stopper1)
		if stopper2 and (piecePinned == False or (d == (-1,-1)or d ==(1,1))):
			moves,stopper2 = get_diagonal_moves(moves,r,c,r-counter,c-counter,board,stopper2)
		if stopper3 and (piecePinned == False or (d == (1,-1)or d ==(-1,1))):
			moves,stopper3 = get_diagonal_moves(moves,r,c,r+counter,c-counter,board,stopper3)
		if stopper4 and (piecePinned == False or (d == (-1,1)or d ==(1,-1))):
			moves,stopper4 = get_diagonal_moves(moves,r,c,r-counter,c+counter,board,stopper4)
		counter = counter + 1
	return moves

def get_diagonal_moves(moves,r,c,x,y,board,stopper):	
	temp_list = [r,c,x,y]
	if stopper and all(i >= 0 and i <=7 for i in temp_list):
		if (board[r][c] == 3 or board[r][c] == 5) and (player_turn.white_to_move is True):
			if board[x][y] not in player_turn.white_pieces:
				moves.append([(r,c),(x,y)])
			else:
				pass
		if (board[r][c] == 9 or board[r][c] == 11) and (player_turn.white_to_move is False):
			if board[x][y] not in player_turn.black_pieces:
				moves.append([(r,c),(x,y)])
			else:
				pass

		if board[x][y] != 0:
			stopper = False
	return moves, stopper