import piece_mover
import valid_moves
import player_turn
import move_undoer 

def get_en_p_pinned(move1,move2,moves):
	piece_mover.move_piece(move1,move2)
	checks,pins,king_row,king_col = valid_moves.get_valid_moves()
	move_undoer.undo_move([(move1,move2)])
	player_turn.white_to_move = not player_turn.white_to_move
	if len(checks) == 0:
		moves.append([move1,move2])
		return moves
	else:
		return moves

