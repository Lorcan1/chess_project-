import player_turn
white_to_move = True
en_passant_bool = False
white_castle_kingside = False
white_castle_queenside = False
black_castle_kingside = False
black_castle_queenside = False
white_promotion = False
black_promotion = False 
kingside_castle_white =False
queenside_castle_white = False
kingside_castle_black = False
queenside_castle_black = False
white_pieces = [1,2,3,4,5,6]
black_pieces = [7,8,9,10,11,12]
taken_square = []
en_p = []
depth2 = 0
import numpy as np
board = np.array([[0 for x in range(8)] for y in range(8)])

def read_fen(board): 	
	player_turn.kingside_castle_white =False
	player_turn.queenside_castle_white = False
	player_turn.kingside_castle_black = False
	player_turn.queenside_castle_black = False
	global white_to_move
	fen_in  = input("Enter fen (type s for start position): ")
	if fen_in == 's':
		fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
	else: 
		fen = fen_in 

	#fen = 'rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR b KQkq - 0 1'
	#fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1' #initial

	d = {'P': 1,'N' : 2,'B' : 3,'R' : 4,'Q' : 5,'K' : 6,'p' : 7,'n' : 8,'b' : 9,'r' : 10,'q' : 11,'k' : 12}

	rank = 0 #row
	file = 0 #column

	for char in fen:
		if char.isdigit() is True:
			file += int(char)
		elif char == '/':
			rank += 1 
			file = 0
		elif char in d.keys():
			board[rank][file] = d.get(char)
			file += 1
		elif char == ' ':
			if (fen[fen.index(char) + 1]) == 'w':
					white_to_move = True 
					break
			elif (fen[fen.index(char)+1]) == 'b':
					print('hi')
					white_to_move = False 
					break

	x = fen.split(" ")
	x.reverse()
	x.pop()
	print(x)
	for string in x: 
		if 'K' in string:
			player_turn.kingside_castle_white =True
		if 'Q' in string:
			player_turn.queenside_castle_white = True
		if 'k' in string:
			player_turn.kingside_castle_black = True
		if 'q' in string:
			player_turn.queenside_castle_black = True

	print(player_turn.kingside_castle_white)
	print(player_turn.kingside_castle_black)
	print(player_turn.queenside_castle_black)
	print(player_turn.queenside_castle_white)

	return board