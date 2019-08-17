import tensorflow as tf
class network():
	def __init__(self):
		self.frame = tf.placeholder(tf.float32, shape = [None,63], name = "frame")
		self.hidden1 = tf.contrib.layers.fully_connected(self.frame, 500)
		self.hidden2 = tf.contrib.layers.fully_connected(self.hidden1, 500)
		self.hidden3 = tf.contrib.layers.fully_connected(self.hidden2, 500)
		self.logits = tf.contrib.layers.fully_connected(self.hidden3, 196, activation_fn = tf.nn.softmax)