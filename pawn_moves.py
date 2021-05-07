
import player_turn


def p_moves(moves,r,c,pins): #add take functionality
	if len(pins) == 0:
		piecePinned = False 
	else:
		for pin in pins:
			if(pin[0] == r and pin[1] == c):
				piecePinned = True 
				d = (pin[2],pin[3])
			else:
				piecePinned = False
	if player_turn.white_to_move ==  True and player_turn.board[r][c] == 1 and player_turn.board[r-1][c] == 0 and r != 0 and (piecePinned is False or d == (-1,0)):
		moves.append([(r,c),(r-1,c)]) #if white decrease
		if r == 6 and player_turn.board[r-2][c] ==0: #if in starting row, can move twice
			moves.append([(r,c),(r-2,c)])
		else:
			pass
	elif player_turn.white_to_move ==  False and  r != 7 and player_turn.board[r][c] == 7 and player_turn.board[r+1][c] == 0 and (piecePinned is False or d == (1,0)):
		moves.append([(r,c),(r+1,c)]) #if black increase
		if r == 1 and player_turn.board[r+2][c] == 0:
			moves.append([(r,c),(r+2,c)])
		else:
			pass
	else:
		pass
# #takes
	if player_turn.white_to_move ==  True and player_turn.board[r][c] == 1 and player_turn.board[r-1][c-1] in player_turn.black_pieces and 0<= r-1 <=7 and 0<= c-1 <=7 and (piecePinned is False or d == (-1,-1)): #take black
		moves.append([(r,c),(r-1,c-1)])
	else:
		pass
	if player_turn.white_to_move ==  True and player_turn.board[r][c] == 1 and c != 7 and player_turn.board[r-1][c+1] in player_turn.black_pieces and 0<= r-1 <=7 and 0<= c+1 <=7 and (piecePinned is False or d == (-1,1)):
		moves.append([(r,c),(r-1,c+1)])
	else:
		pass

	if player_turn.white_to_move ==  True and  r == 3 and player_turn.board[r][c] == 1 and (r,c-1)in player_turn.en_p and (piecePinned is False): 
		moves.append([(r,c),(r-1,c-1)])
	elif player_turn.white_to_move ==  True and  r == 3  and player_turn.board[r][c] == 1 and (r,c+1) in player_turn.en_p and (piecePinned is False): 
		moves.append([(r,c),(r-1,c+1)])

	if player_turn.white_to_move ==  False and  r != 7 and player_turn.board[r][c] == 7 and player_turn.board[r+1][c-1] in player_turn.white_pieces and 0<= r+1 <=7 and 0<= c-1 <=7 and (piecePinned is False or d == (1,-1)): #take white
		moves.append([(r,c),(r+1,c-1)])
	else:
		pass
	if  player_turn.white_to_move ==  False and r != 7 and  player_turn.board[r][c] == 7 and c != 7 and player_turn.board[r+1][c+1] in player_turn.white_pieces and 0<= r+1 <=7 and 0<= c+1 <=7 and (piecePinned is False or d == (1,1)):
		moves.append([(r,c),(r+1,c+1)])
	else:
		pass
	if player_turn.white_to_move ==  False and  r == 4  and player_turn.board[r][c] == 7  and (r,c-1)in player_turn.en_p and (piecePinned is False): 
		moves.append([(r,c),(r+1,c-1)])
	elif player_turn.white_to_move ==  False and  r == 4  and player_turn.board[r][c] == 7 and (r,c+1) in player_turn.en_p and (piecePinned is False): 
		moves.append([(r,c),(r+1,c+1)])

	return moves