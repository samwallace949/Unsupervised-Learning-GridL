import numpy as np
import tensorflow as tf
import threading
import time
import json
import os
from gridL_agents import agent
from gridL_buffer import experience_buffer
from gridL_buffer import buffer_image
from gridL_game import gameData
import threading
path = "./saved-models"
model_desc_file = "saved_run_backlog.txt"
def time_string():
	t = time.gmtime()
	s = ""
	s = str(t[1]) + "." + str(t[2]) + "." + str(t[0]) + "_" + str(t[3]) + ":" + str(t[4]) + ":" + str(t[5])
	return s
def max(a,b):
	if a>b:
		return a
	return b
def generate_frames(buffer, n_frames, n_threads):
	init_cap = buffer.size()
	frames_per_thread = n_frames/n_threads
	threads = []
	for i in range (0, n_threads):
		if(i == 0):
			t = threading.Thread(target = gen_frames_worker, args = (buffer, frames_per_thread + (n_frames % n_threads),), daemon = True)
		else:
			t = threading.Thread(target = gen_frames_worker, args = (buffer, frames_per_thread,), daemon = True)
		threads.append(t)
		t.start()
	while buffer.size()-init_cap < n_frames:
		time.sleep(1)
		print(str(buffer.size()-init_cap) + " rounds completed")
def gen_frames_worker(buffer, n_frames):
	game = gameData(100)
	b = experience_buffer(n_frames)
	worker = agent(b, game, 1)
	for i in range(0, int(n_frames)):
		worker.make_action(1)
	for j in range (0, int(n_frames)):
		buffer.add_frame(b.buffer[j])

###### ^^^^^ VARIOUS STATIC METHODS AND VARIABLES ^^^^^ ######
		
if not os.path.exists(path):
    os.makedirs(path)
while True:	
	tf.reset_default_graph()	
	game = gameData(100)
	b = experience_buffer(1000000)
	random_player = agent(experience_buffer(1000000), game, 1)
	trainables = tf.trainable_variables()
	trained_player = agent(b, game, 0.5)
	saver = tf.train.Saver()
	load_model, train_model = 'n', 'y'
	#a = input("load model?")
	#b = input("train model?")
	if(load_model == 'y'):
			cpkt = tf.train.get_checkpoint_state(path)
			#saver.restore(trained_player.sess,cpkt.model_checkpoint_path)
	if(train_model == 'y'):
		init_time = time.time()
		for i in range (0, 400000):
			trained_player.make_action(1)
			if((i+1)%1000 == 0):
				print("{} rounds completed".format(i))
		#generate_frames(b, 20000, 8)
		print("generating frames took {} seconds".format(time.time() - init_time))
		for k in range (0, 30):
			print("{} epochs completed".format(k))
			trained_player.train(0, 10000, 1000)
	game.reset_game()
	rand_wins, trained_wins = 0,0
	num_games = 100
	for j in range (0, num_games):
		game.reset_game()
		turn,c = 0,0
		while game.is_over() == 0:
			if(turn == 0):
				trained_player.make_action(0)
				turn = 1
			else:
				random_player.make_action(1)
				turn = 0
		if(turn == 1):
			if(game.is_over() == 2):
				trained_wins += 1
				print ("Trained Win!")
			else:
				rand_wins += 1
				print("Rand win")
		else:
			if(game.is_over() == 2):
				rand_wins += 1
				print("Rand win")
			else:
				trained_wins += 1
				print ("Trained Win!")
	print("After {} games, the agent trained for 150,000 steps has a win ratio of {} to {} against a randomly playing agent".format(num_games, trained_wins, rand_wins))
	description = "400 thousand frames made randomly, 300 thousand trained randomly, updated training net every 1000 frames"
	print(description)
	print(time_string())
	if(num_games-trained_wins < 10):
		run_name = 0.04
		saver.save(trained_player.sess,path+'/model-'+str(run_name)+'.ckpt')
		print("Saved Model")
		opp_name = "Random"
		s = "\n\n\n\nName of Run: {}\nName of Opponent: {}\nDescription: {}\nDate and Time of Run: {}\nWins: {}\nLosses: {}\n".format(run_name, opp_name, description, time_string(), trained_wins, rand_wins)
		f = open(model_desc_file, "r")
		existing_data = f.read()
		f.close()
		f = open(model_desc_file, "w")
		f.write(existing_data+s)
		f.close()
		exit()