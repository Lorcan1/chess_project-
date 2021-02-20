import numpy as np 
import sys
import random

import pprint



# def game_checker(game_over):
# 	king_alive = king_checker(king_alive) 

# 	if king_alive is True:
# 		return True
# 	else:
# 		return False 

# game_over = 1		
# game_over = game_checker(game_over)

# if game_over is False:
# 	pass
# else:
# 	print('Game is over')
# 	sys.ext()




# def king_checker(king_checker):


# def knight_move(knight_position):
	




board = np.arange(64)


board[0] = 10
board[1] = 8
board[2] = 9
board[3] = 11
board[4] = 12
board[5] = 9
board[6] = 8
board[7] = 10
board[8] = 7
board[9] = 7
board[10] = 7
board[11] = 7
board[12] = 7
board[13] = 7
board[14] = 7
board[15] = 7


board[48] = 1
board[49] = 1
board[50] = 1
board[51] = 1
board[52] = 1
board[53] = 1
board[54] = 1
board[55] = 1
board[56] = 4
board[57] = 2
board[58] = 3
board[59] = 5
board[60] = 6
board[61] = 3
board[62] = 2
board[63] = 4



board_d = {




0: 4,
1 : 2,
2 : 3,
3 : 5,
4 : 6,
5 : 3,
6 : 2,
7 : 4,
8 : 1,
9 : 1,
10 :1,
11 : 1,
11 : 1,
12 : 1,
13 : 1,
14 : 1,
15 : 1,




16: 0,
17: 0,
18: 0,
19: 0,
20: 0,
21: 0,
22: 0,
23: 0,
24: 0,
25: 0,
26: 0,
27: 0,
28: 0,
29: 0,
30: 0,
31: 0,
32: 0,
33: 0,
34: 0,
35: 0,
36: 0,
37: 0,
38: 0,
39: 0,
40: 0,
41: 0,
42: 0,
43: 0,
44: 0,
45: 0,
46: 0,
47: 0,
48: 0,


48 : 10,
49 : 8,
50 : 9,
51: 11,
52: 12,
53 : 9,
54 : 8,
55 : 10,
56 : 7,
57 : 7,
58 : 7,
59 : 7,
60 : 7,
61 : 7,
62 : 7,
63 : 7,

}



def make_move():  #pick a random piece to move 
	x = random.randint(1, 6)
	y = random.randint(7, 12)
	return x,y 
x,y = make_move() 

x= 4
y =10
#find new key to move piece to


def move(x,y, d):  #need to find their original square 



	key_list = list(d.keys())
	val_list = list(d.values())


	if x is 1: #pawn
		move = random.randint(1, 2)
		position = val_list.index(x) + move

		d[position] = x


	elif x is 2: #knighy  BROKEN can move from one staring position tp another

		new_row = random.choice([8,16])

		if new_row is 8:
			new_column = random.choice([-2,2])
		else:
			new_column = random.choice([-1,1])

		move = new_row + new_column
		position = val_list.index(x) + move



		d[position] = x



	elif x is 3: #bishop  INCOMPLETE, only one move forward
		move= random.choice([7,9])

		position = val_list.index(x) + move
		d[position] = x

	elif x is 4: #rook  INCOMPLETE, only one move forward
		move= random.choice([8,16])

		position = val_list.index(x) + move

		if d[position] is not 0:
			return(d, True )
		else:
			d[position] = x

	elif x is 5: #queen INCOMPLETE, only one move forward (same as rook)
		move = 8

		position = val_list.index(x) + move
		d[position] = x

	elif x is 6: #queen INCOMPLETE, only one move forward (same as rook)
		move = 1

		position = val_list.index(x) + move
		d[position] = x


	d[val_list.index(x)] = 0

	return(d, False)

board_d, retake = move(x,y,board_d)



#pprint.pprint(board_d) 	
print(x)


#TO DO
#function from position down #
#has to check for every space that passes is empty