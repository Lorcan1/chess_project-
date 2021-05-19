import piece_mover,player_turn
from main import resolve_checks,undo_move
import castle 
import valid_moves

player_turn.read_fen(player_turn.board)
move_log  = []
move_log_2 = []


v_moves, checks = resolve_checks()
v_moves = castle.castling(v_moves,move_log,checks)

checks5,pins, king_row, king_col = valid_moves.get_valid_moves(player_turn.board,0,3)


print(len(checks5))

