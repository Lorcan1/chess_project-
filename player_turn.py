white_to_move = True
white_pieces = [1,2,3,4,5,6]
black_pieces = [7,8,9,10,11,12]
taken_square = []
en_p = []
import numpy as np
board = np.array([[0 for x in range(8)] for y in range(8)])

def read_fen(board): 	
	fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

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
			elif (fen[fen.index(char)+1])== 'b':
					white_to_move = False 
					break
	return board