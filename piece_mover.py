import player_turn

def move_piece(old_square, new_square):
	old_row,old_col,new_row,new_col = old_square[0], old_square[1],new_square[0],new_square[1]
	old_row, old_col,new_row,new_col  = int(old_row), int(old_col),int(new_row),int(new_col)
	en_passant_take(old_row, old_col,new_row, new_col)
	check_en_Passant(old_row, old_col,new_row,new_col) 
	check_castle(old_row,old_col,new_row,new_col)
	check_promotion(old_row,old_col,new_row,new_col)
	temp = player_turn.board[old_row, old_col]
	player_turn.taken_square.append(player_turn.board[new_row][new_col])
	temp = int(temp)
	player_turn.board[new_row, new_col] = temp 
	player_turn.board[old_row, old_col] = 0
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
	if (player_turn.white_to_move is True) and (r ==2) and player_turn.board[r][c] == 0 and  (len(player_turn.en_p)!= 0) and (r - old_r == -1) and (((old_r,old_c-1) in player_turn.en_p) or ((old_r,old_c+1) in player_turn.en_p)) and (old_c - c == -1 or old_c - c == 1) and c == player_turn.en_p[0][1]:
		player_turn.board[player_turn.en_p[0][0]][player_turn.en_p[0][1]] = 0
		white_en_passant_bool = True
		black_en_passant_bool = False

	elif (player_turn.white_to_move is False) and player_turn.board[r][c] == 0 and (r ==5) and (len(player_turn.en_p)!= 0) and (r - old_r == 1) and (((old_r,old_c-1) in player_turn.en_p) or ((old_r,old_c+1) in player_turn.en_p)) and (old_c - c == -1 or old_c - c == 1) and c == player_turn.en_p[0][1]:
		player_turn.board[player_turn.en_p[0][0]][player_turn.en_p[0][1]] = 0
		black_en_passant_bool = True
		white_en_passant_bool = False
	else:
		white_en_passant_bool = False
		black_en_passant_bool = False
	player_turn.en_p = []
	player_turn.white_en_p_list.append(white_en_passant_bool)
	player_turn.black_en_p_list.append(black_en_passant_bool)

	return

def check_promotion(old_r,old_c,r,c):
	if player_turn.white_to_move is True and player_turn.board[old_r][old_c] == 1 and r == 0:
		player_turn.board[old_r][old_c] = 5
		white_promotion = True
		black_promotion = False
	elif player_turn.white_to_move is False and player_turn.board[old_r][old_c] == 7 and r == 7:
		player_turn.board[old_r][old_c] = 11
		black_promotion = True
		white_promotion = False
	else:
		white_promotion = False
		black_promotion = False
	player_turn.white_promotion_list.append(white_promotion)
	player_turn.black_promotion_list.append(black_promotion)

	return

def check_castle(old_r,old_c,r,c):
	if player_turn.board[old_r][old_c] == 6: #white
		if old_r == 7 and old_c == 4:
			if r == 7 and c == 2: #queenside
				player_turn.board[7][0] = 0
				player_turn.board[7][3] = 4
			elif r == 7 and c == 6: #kingside
				player_turn.board[7][7] = 0
				player_turn.board[7][5] = 4
			else:
				pass
	elif player_turn.board[old_r][old_c] == 12:
		if old_r ==0 and old_c ==4:
			if r == 0 and c == 2:
				player_turn.board[0][0] = 0
				player_turn.board[0][3] = 10
			elif r == 0 and c == 6:
				player_turn.board[0][7] = 0
				player_turn.board[0][5] = 10
			else:
				pass
	return