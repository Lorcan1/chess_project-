import player_turn

def get_king_location(board):
	for i in range(len(board)):
		for j in range(len(board[i])):
			if (player_turn.white_to_move is True) and (board[i][j] == 6):
				king_row = i
				king_col = j
			elif (player_turn.white_to_move is False) and (board[i][j] == 12): #get all king moves 
				king_row = i
				king_col = j
	return king_row,king_col

def get_valid_moves(board, x=100,y=0): 
	directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)) #up,down,left,right , four diagonals
	checks = []
	pins = []
	if x == 100:
		king_row,king_col = get_king_location(board)
	else:
		king_row = x
		king_col = y
	for j in range(len(directions)):
		possible_pin = ()
		direction = directions[j]
		row = king_row
		column = king_col
		counter = 1
		ally_counter = 0
		enemy_counter = 0
		for i in range(1,8):
			row = king_row + (direction[0]*i)
			column = king_col + (direction[1]*i)
			if ally_counter <2 and enemy_counter < 1:	
				if (0<=row<=7) and (0<=column<=7):
					if board[row][column] == 0:
						pass
					elif (player_turn.white_to_move == False and board[row][column] in player_turn.black_pieces) or (player_turn.white_to_move == True and board[row][column] in player_turn.white_pieces): 
						ally_counter = ally_counter + 1
						if possible_pin == ():
							possible_pin = (row,column,direction[0],direction[1])
						else:
							break
					elif (player_turn.white_to_move == False and board[row][column] in player_turn.white_pieces) or (player_turn.white_to_move == True and board[row][column] in player_turn.black_pieces): 
						enemy_counter = enemy_counter + 1 
						if (i == 1) and ((board[row][column] == 1 and (6<=j<=7)) or (board[row][column] == 7 and (4<=j<=5))):
							if ally_counter == 0: # add conditions in which pawn is checking king
								checks.append((row,column,direction[0],direction[1]))
							elif ally_counter == 1:
								break
						elif (4<=j<=7) and (board[row][column] == 3 or board[row][column] == 9):
							if ally_counter == 0:
								checks.append((row,column,direction[0],direction[1]))
							elif ally_counter == 1:
								pins.append(possible_pin)
						elif (0<=j<=3) and (board[row][column] == 4 or board[row][column] == 10):
							if ally_counter == 0:
								checks.append((row,column,direction[0],direction[1]))
							elif ally_counter == 1:
								pins.append(possible_pin)
						elif board[row][column] == 5 or board[row][column] == 11:
							if ally_counter == 0:
								checks.append((row,column,direction[0],direction[1]))
							elif ally_counter == 1:
								pins.append(possible_pin)
						elif (i ==1) and (board[row][column] == 6 or board[row][column] == 12): 
							if ally_counter == 0: # add conditions in which pawn is checking king
								checks.append((row,column,direction[0],direction[1]))
							elif ally_counter == 1:
								break
						else:
							break
			else:
				break
	knight_moves = [(-2,-1),(-1,-2),(-1,2),(-2,1),(2,-1),(1,-2),(1,2),(2,1)] #seperate loop needed for knight moves
	for move in knight_moves:
		if 0<= king_row+move[0] <=7 and 0<= king_col+move[1] <=7:
			if board[king_row][king_col] == 12 and board[king_row+move[0]][king_col+move[1]] == 2: # and player_turn.white_to_move?
				checks.append((king_row+move[0],king_col+move[1]))
			elif board[king_row][king_col] == 6 and board[king_row+move[0]][king_col+move[1]] == 8:
				checks.append((king_row+move[0],king_col+move[1]))
	return checks,pins,king_row,king_col