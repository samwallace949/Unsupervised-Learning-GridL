import tensorflow as tf
class network():
	def __init__(self):
		self.frame = tf.placeholder(tf.float32, shape = [None,63], name = "frame")
		self.hidden1 = tf.contrib.layers.fully_connected(self.frame, 196)
		self.hidden2 = tf.contrib.layers.fully_connected(self.hidden1, 196)
		self.logits = tf.contrib.layers.fully_connected(self.hidden2, 196, activation_fn = tf.nn.softmax)