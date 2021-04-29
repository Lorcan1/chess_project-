import random
import main

piece_scores = {1:1,7:1,2:3,8:3,3:3,9:3,4:5,10:5,5:9,11:9,6:0,12:0}
checkmate = 1000
stalemate = 0

def find_random_move(valid_moves):#picks and returns a random move 
#
	return valid_moves[random.randint(0,len(valid_moves)-1)] #inclusive of both	values



def find_best_move(board, valid_moves):
	turn_multiplier = 1 if main.white_to_move == True else - 1 
	opponent_min_max_score = -checkmate
	best_player_move = None 
	for player_move in valid_moves:
		#make the move  
		#get opponent moves
		#make opponent move
		#find opponents max score 
			#if checkmate:
				#score  = -turn_multiplier * checkmate
			#elif stalemate
				#score = stalemate (0)
			#else:
				#score = -turn_multiplier * score_material(board)
			#calculate the score, multiply by -turn multiplier 
			if score > opponent_max_score:
				opponent_max_score = score
			#undo opponent move 
			if opponent_max_score < opponent_min_max_score:
				opponent_min_max_score = opponent_max_score
				best_player_move - player_move
			#undo the move
	return best_player_move
	 
 
#minimise opponent score while maximising our own 
#search for opponents worst best move (minimum maximum score)


def score_material(board):
	score = 0 
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] <= 6:
				score += piece_scores[board[i][j]]
			elif board[i][j] >= 7:
				score -= piece_scores[board[i][j]]
	return score 
