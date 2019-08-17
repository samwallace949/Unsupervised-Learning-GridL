from gridL_network import network
import tensorflow as tf
import numpy as np
from gridL_buffer import buffer_image
import threading
class agent ():
	def __init__(self, session, buffer, game, target_update_rate, leader_network = None):
		self.game = game
		a = len(tf.trainable_variables())
		self.training_network = network() # stationary network that determines the loss value
		self.training_vars = tf.trainable_variables()[a:]
		a = len(tf.trainable_variables())
		self.target_network = network() # takes actions within the environment to fill the experience buffer, learns online with every so many actions
		self.target_vars = tf.trainable_variables()[a:]
		print("Length of training and target networks respectively are {} and {}".format(len(self.training_vars), len(self.target_vars)))
		self.sess = session
		self.buffer = buffer
		self.leader_network = leader_network
		self.u_ops = []
		self.lead_ops = []
		for i, tensor in enumerate(self.training_vars):
			self.u_ops.append(tensor.assign((target_update_rate * self.target_vars[i].value())+((1-target_update_rate) * tensor.value())))
		if(self.leader_network != None):
			for i, tensor in enumerate(self.training_vars):
				self.lead_ops.append(tensor.assign((self.leader_network.training_vars[i].value())))
			for i, tensor in enumerate(self.target_vars):
				self.lead_ops.append(tensor.assign((self.leader_network.target_vars[i].value())))
		self.r,self.a = tf.placeholder(dtype = tf.float32),tf.placeholder(dtype = tf.int32)
		self.x = (np.max(self.training_network.logits)) + self.r
		self.y = self.target_network.logits[0][a]
		self.loss = tf.square(tf.subtract(self.x,self.y))
		self.optimizer = tf.train.AdamOptimizer(0.01)
		self.train_op = self.optimizer.minimize(self.loss, var_list = self.target_vars)
	def get_logits(self):
		return self.sess.run(self.target_network.logits, feed_dict = {self.target_network.frame: [self.game.make_frame().flatten()]})
	def make_action(self, prob_rand):
		initial_score_difference = self.game.score[0, 0] - self.game.score[0, 1] # calculates initial score delta
		o_s = self.game.make_frame()
		logits = np.random.rand(1,196)[0]
		if(prob_rand < np.random.rand()):
			logits = np.copy(self.get_logits()[0])
		final_action = -1
		c = 0
		while True:
			action = np.argmax(logits)
			if(c > 196):
				logits = np.random.rand(1,196)[0]
				c = 0
			else:
				c += 1
			piece = int(action/49)
			position = action % 49
			p_x = int(position/7)
			p_y = position%7
			if(self.game.place_piece(piece, [p_x, p_y], False) == True):
				final_action = action
				break
			else:
				logits[np.argmax(logits)] = 0
		final_score_difference = self.game.score[0, 0] - self.game.score[0, 1]
		reward = final_score_difference - initial_score_difference
		self.buffer.add_frame(buffer_image(o_s, final_action, reward, self.game.make_frame()))
		self.game.rotate_game()	
	def train(self, prob_reward_frame, num_frames, frames_until_reset):
		for i in range (0, num_frames):
			f = self.buffer.peek_frame_random()
			if(np.random.random() < prob_reward_frame):
				f = self.buffer.peek_frame_random_reward_threshold()
			self.sess.run(self.train_op, feed_dict = 
			{self.target_network.frame: [f.o_s.flatten()], 
			self.training_network.frame:[f.n_s.flatten()], 
			self.r: float(f.r), 
			self.a: int(f.a)}
			)
			if(i % frames_until_reset == 0):
				self.update_training_net()
	def update_training_net(self):
		for i, op in enumerate(self.u_ops):
			self.sess.run(op)
	def update_to_lead_network(self):
		for i, op in enumerate(self.lead_ops):
			self.sess.run(op)
