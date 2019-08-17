import numpy as np

pieces = ([[0,0],[0,1], [1,0]],[[0,0],[0,1], [-1,0]], [[0,0],[0,-1], [1,0]], [[0,0],[0,-1],[-1,0]])

#	0:		1:		2:		3:
#		11		11		1		 1
#		1		 1 		11		11
#
#

class gameData ():
	def __init__(self, win_score):
		self.win_score = win_score
		self.board = np.zeros([7,7])
		self.options1 = np.zeros([1, 7])
		self.options2 = np.zeros([1, 7])
		self.score = np.zeros([1, 2])
	def reset_game(self):
		self.board = np.zeros([7,7])
		self.options1 = np.zeros([1, 7])
		self.options2 = np.zeros([1, 7])
		self.score = np.zeros([1, 2])
	def place_piece(self, piece, position, print_error):
		if (self.options1[0, piece] != 0):
			if(print_error == True):
				print("Invalid Piece selection")
			return False
		if self.is_valid_location(piece, position) == False:
			if(print_error == True):
				print("Invalid Piece Location")
			return False
		for i in range(0,3):
			self.board[position[0]+pieces[piece][i][0], position[1] + pieces[piece][i][1]] = 1#change values of the board
		self.options1[0, piece] = 1
		self.reset_possible_pieces()
		self.remove_rows()
		self.fullness_check()
		return True
	def reset_possible_pieces(self):
		for i in range(0,4):
			if(self.options1[0, i] == 0):
				break
			if(i == 3):
				for j in range(0, 4):
					self.options1[0, j] = 0
	def fullness_check(self):
		for i in range(0, 7):
			for j in range(0, 7):
				for k in range(0,4):
					if self.options2[0, k] == 1:
						continue
					if(self.is_valid_location(k, [i,j]) == True):
						return
		self.board = np.zeros([7,7])
	def remove_rows(self):
		rowList = []
		columnList = []
		hasRow = True
		hasColumn = True
		for i in range (0, 7):
			for j in range(0,7):
				if(self.board[i][j] == 0):
					hasRow = False
				if(self.board[j][i] == 0):
					hasColumn = False
			if(hasRow == True):
				rowList.append(i)
			if(hasColumn == True):
				columnList.append(i)
			hasRow = True
			hasColumn = True
		for i in range (0, len(rowList)):
			self.score[0,0] += 1
			for j in range(0, 7):
				self.board[rowList[i]][j] = 0
		for i in range (0, len(columnList)):
			self.score[0,1] += 1
			for j in range(0, 7):
				self.board[j][columnList[i]] = 0
	def make_frame(self):
		ans = np.concatenate((self.board, self.options1, self.options2))
		return ans
	def is_valid_location(self, piece, position):
		for i in range(0,3):
			if position[0] + pieces[piece][i][0] >= 7 or position[0] + pieces[piece][i][0] < 0 or position[1] + pieces[piece][i][1] >= 7 or position[1] + pieces[piece][i][1] < 0 or self.board[position[0]+pieces[piece][i][0], position[1] + pieces[piece][i][1]] == 1:
				return False
		return True
	def rotate_game (self): # symmetric function
		n_board = np.zeros([7,7])
		for i in range (0, 7):
			for j in range (0, 7):
				n_board[i,j] = self.board[j,i]
		self.board = n_board
		temp_options = np.zeros([2,7])
		temp_options[0, 0] = self.options2[0, 0]
		temp_options[0, 1] = self.options2[0, 2]
		temp_options[0, 2] = self.options2[0, 1]
		temp_options[0, 3] = self.options2[0, 3]
		temp_options[1, 0] = self.options1[0, 0]
		temp_options[1, 1] = self.options1[0, 2]
		temp_options[1, 2] = self.options1[0, 1]
		temp_options[1, 3] = self.options1[0, 3]
		b = np.split(temp_options, 2)
		self.options1 = b[0]
		self.options2 = b[1]
		a = self.score[0,0]
		self.score[0,0] = self.score[0,1]
		self.score[0,1] = a
	def is_over(self):
		if(self.score[0,0] >= self.win_score):
			return 1
		elif(self.score[0,1] >= self.win_score):
			return 2
		else:
			return 0
