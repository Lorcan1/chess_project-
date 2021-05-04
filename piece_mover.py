import player_turn

def move_piece(old_square, new_square):
	old_row,old_col,new_row,new_col = old_square[0], old_square[1],new_square[0],new_square[1]
	old_row, old_col,new_row,new_col  = int(old_row), int(old_col),int(new_row),int(new_col)
	en_passant_take(old_row, old_col,new_row, new_col)
	check_en_Passant(old_row, old_col,new_row,new_col) 
	check_castle(old_row,old_col,new_row,new_col)
	check_promotion(old_row,old_col,new_row,new_col)
	temp = player_turn.board[old_row:old_row+1, old_col:old_col+1]
	player_turn.taken_square.append(player_turn.board[new_row][new_col])
	if temp == 0: 
		pass
	else:
		temp = int(temp)
		player_turn.board[new_row:new_row+1, new_col:new_col+1] = temp 
		player_turn.board[old_row:old_row+1, old_col:old_col+1] = 0
	return 

def check_en_Passant(old_row, old_col,new_row,new_col): 
	if player_turn.white_to_move is False and player_turn.board[old_row][old_col] == 7:
		if old_row == 1 and new_row == 3:
			player_turn.en_p.append((new_row, new_col))
		else:
			pass
	elif player_turn.white_to_move is True and player_turn.board[old_row][old_col] == 1:
		if old_row == 6 and new_row == 4:
			player_turn.en_p.append((new_row, new_col))
		else:
			pass
	else:
		pass 
	return 

def en_passant_take(old_r,old_c ,r,c):
	#en_passant_take removes the opponents piece from the board when the player plays en passant
	if (player_turn.white_to_move is True) and (len(player_turn.en_p)!= 0) and (r - old_r == -1) and (((old_r,old_c-1) in player_turn.en_p) or ((old_r,old_c+1) in player_turn.en_p)) and (old_c - c == -1 or old_c - c == 1) and c == player_turn.en_p[0][1]:
		player_turn.board[player_turn.en_p[0][0]][player_turn.en_p[0][1]] = 0
		player_turn.en_passant_bool = True
	elif (player_turn.white_to_move is False) and (len(player_turn.en_p)!= 0) and (r - old_r == 1) and (((old_r,old_c-1) in player_turn.en_p) or ((old_r,old_c+1) in player_turn.en_p)) and (old_c - c == -1 or old_c - c == 1) and c == player_turn.en_p[0][1]:
		player_turn.board[player_turn.en_p[0][0]][player_turn.en_p[0][1]] = 0
		player_turn.en_passant_bool = True
	player_turn.en_p = []

	return

def check_promotion(old_r,old_c,r,c):
	if player_turn.white_to_move is True and player_turn.board[old_r][old_c] == 1 and r == 0:
		player_turn.board[old_r][old_c] = 5
	elif player_turn.white_to_move is False and player_turn.board[old_r][old_c] == 7 and r == 7:
		player_turn.board[old_r][old_c] = 11
	else:
		pass
	return

def check_castle(old_r,old_c,r,c):
	if player_turn.board[old_r][old_c] == 6: 
		if old_r == 7 and old_c == 4:
			if r == 7 and c == 2:
				player_turn.board[7][0] = 0
				player_turn.board[7][3] = 4
				player_turn.white_castle_queenside = True
			elif r == 7 and c == 6:
				player_turn.board[7][7] = 0
				player_turn.board[7][5] = 4
				player_turn.white_castle_kingside = True
			else:
				pass
	elif player_turn.board[old_r][old_c] == 12:
		if old_r ==0 and old_c ==4:
			if r == 0 and c == 2:
				player_turn.board[0][0] = 0
				player_turn.board[0][3] = 10
				player_turn.black_castle_queenside = True
			elif r == 0 and c == 6:
				player_turn.board[0][7] = 0
				player_turn.board[0][5] = 10
				player_turn.black_castle_kingside = True
			else:
				pass
	return