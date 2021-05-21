import piece_mover,player_turn
from main import resolve_checks,undo_move
import castle
import csv

player_turn.read_fen(player_turn.board)
print(player_turn.white_to_move)
move_log  = []
move_log_2 = []
move_log_3 = []

def move_generation_test(depth,move=0,prev=0):
	if depth ==0:
		move_log_3.append(move)
		return 1

	v_moves, checks = resolve_checks()
	v_moves = castle.castling(v_moves,move_log,checks)

	num_positions = 0
	
	for move in v_moves:
		piece_mover.move_piece(move[0], move[1])
		player_turn.white_to_move = not player_turn.white_to_move
		num_positions += move_generation_test(depth -1,move)
		move_log.append(move)
		if depth == player_turn.depth2:
			y = num_positions - prev
			notate = rename_notation(move[0],move[1])
			print(move[0],move[1],notate,y)
			prev = num_positions
		
		undo_move(move_log)

	return num_positions


# def move_generation_test2(depth,move=None,prev=0): #has to be position2 , depth 3 
# 	if depth ==0:
# 		move_log_2.append(move)
# 		return 1
# 	if depth == player_turn.depth2:
# 		v_moves = [[(7, 4) ,(7, 2)]]
# 	# elif depth == (player_turn.depth2-1):
# 	# 	v_moves =[[(0,0),(0,2)]]
# 	else:
# 		v_moves, checks = resolve_checks()
# 		v_moves = castle.castling(v_moves,move_log,checks)

# 	num_positions = 0
# 	print(player_turn.board)
# 	for move in v_moves:
# 		piece_mover.move_piece(move[0], move[1])
# 		player_turn.white_to_move = not player_turn.white_to_move
# 		num_positions += move_generation_test2(depth -1,move)
# 		move_log.append(move)
# 		if depth == (player_turn.depth2-1):
# 			y = num_positions - prev
# 			notate = rename_notation(move[0],move[1])
# 			print(move[0],move[1],notate,y)
# 			prev = num_positions
		
# 		undo_move(move_log)
# 	return num_positions

def rename_notation(move1,move2):
	d1 = {0:'a',1:'b',2:'c' ,3:'d',4:'e',5:'f',6:'g',7:'h'}
	d2 = {0:8,1:7,2:6 ,3:5,4:4,5:3,6:2,7:1}

	return d1[move1[1]] + str(d2[move1[0]]) + d1[move2[1]] + str(d2[move2[0]]) 
depth = input("Enter depth: ")
depth = int(depth)
player_turn.depth2 = depth 
x= move_generation_test(depth)
print(x)