import piece_mover,player_turn
from main import resolve_checks,undo_move

player_turn.read_fen(player_turn.board)
print(player_turn.white_to_move)
# print(player_turn.board)
move_log  = []
move_log_2 = []

def move_generation_test(depth,prev=0):
	if depth ==0:
		return 1
	#print(player_turn.board)

	v_moves, checks = resolve_checks()
	num_positions = 0
	
		
	#print(len(v_moves))
	for move in v_moves:
		piece_mover.move_piece(move[0], move[1])
		player_turn.white_to_move = not player_turn.white_to_move
		num_positions += move_generation_test(depth -1)
		move_log.append(move)
		if depth == player_turn.depth2:
			y = num_positions - prev
			notate = rename_notation(move[0],move[1])
			print(move[0],move[1],notate,y)
			prev = num_positions

		if player_turn.board[5][2] == 2:
			move_log_2.append(move)

		
		undo_move(move_log)

	return num_positions



def rename_notation(move1,move2):
	d1 = {0:'a',1:'b',2:'c' ,3:'d',4:'e',5:'f',6:'g',7:'h'}
	d2 = {0:8,1:7,2:6 ,3:5,4:4,5:3,6:2,7:1}

	return d1[move1[1]] + str(d2[move1[0]]) + d1[move2[1]] + str(d2[move2[0]]) 
depth = input("Enter depth: ")
depth = int(depth)
player_turn.depth2 = depth 
x= move_generation_test(depth)
print(x)
#print(move_log_2)

