import piece_mover,player_turn
from main import resolve_checks,undo_move

player_turn.read_fen(player_turn.board)
move_log  = []
player_turn.white_to_move = False

def move_generation_test(depth,prev):
	if depth ==0:
		return 1

	v_moves, checks = resolve_checks()
	num_positions = 0
	
	#print(len(v_moves))
	for move in v_moves:
		piece_mover.move_piece(move[0], move[1])
		player_turn.white_to_move = not player_turn.white_to_move
		num_positions += move_generation_test(depth -1,0)
		if depth == 5:
			y = num_positions - prev
			print(move[0],move[1],y)
			prev = num_positions
		move_log.append(move)
		undo_move(move_log)

	return num_positions

x= move_generation_test(5,0)
print(x)
