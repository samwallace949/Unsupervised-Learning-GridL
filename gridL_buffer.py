import numpy as np
class buffer_image(object):
	def __init__(self, o_s, a, r, n_s):
		self.o_s = o_s
		self.a = a
		self.r = r
		self.n_s = n_s
		
class experience_buffer ():
	def __init__(self, capacity):
		self.c = capacity
		self.buffer = []
		self.counter = 0
		self.r_buffer = []
	def size (self):
		return len(self.buffer)
	def add_frame(self, frame):
		if self.size() < self.c:
			self.buffer.append(frame)
			if frame.r != 0:
				self.r_buffer.append(self.size()-1)
		else:
			self.buffer[self.counter] = frame
			if frame.r != 0:
				self.r_buffer.append(self.counter)
			self.counter = (self.counter + 1) % self.size()
		
	def peek_frame_random_reward_threshold(self):
		r = np.random.randint(0, len(self.r_buffer))
		return self.buffer[self.r_buffer[r]]
	def peek_frame_random(self):
		r = np.random.randint(0, self.size())
		return self.buffer[r]
	def peek_frame_index(self, r):
		if r >= 0 and r < self.c:
			return self.buffer[r]
		return -1
	def print_frame(self, r):
		f = self.buffer[r]
		print(f.o_s)
		print ("\n")
		print(f.a)
		print ("\n")
		print(f.r)
		print ("\n")
		print(f.n_s)