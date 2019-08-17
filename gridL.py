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
game = gameData(100)
buffer = experience_buffer(1000000)
sess = tf.Session()
player2 = agent(sess, buffer, game, 0.5)
player1 = agent(sess, buffer, game, 0.5, player2)
sess.run(tf.initializers.global_variables())
trainables = tf.trainable_variables()
saver = tf.train.Saver()
print(player1.lead_ops)
load_model, train_model = "n", "y"
#a = input("load model? (y/n)")
#b = input("train model? (y/n)")
opponent_is_random = True
while True:		
	if(load_model == "y"):
			cpkt = tf.train.get_checkpoint_state(path)
			#saver.restore(player2.sess,cpkt.model_checkpoint_path)
	if(train_model == "y"):
		init_time = time.time()
		for i in range (0, (50000, 200000)[opponent_is_random]):
			if opponent_is_random:
				player2.make_action(1)
			else:
				player2.make_action(0.5)
			if((i+1)%1000 == 0):
				print("{} rounds completed".format(i))
		print("generating frames took {} seconds".format(time.time() - init_time))
		for k in range (0, (20, 10)[opponent_is_random]):
			print("{} epochs completed".format(k))
			player2.train(0, 10000, 2000) #training loop should be moved out of conditional after testing
	game.reset_game()
	rand_wins, trained_wins = 0,0
	num_games = 100
	for j in range (0, num_games):
		game.reset_game()
		turn,c = 0,0
		while game.is_over() == 0:
			if(turn == 0):
				if(opponent_is_random):
					player2.make_action(0.1)
				turn = 1
			else:
				if(opponent_is_random == True):
					player1.make_action(1)
				else:
					player1.make_action(0.1)
				turn = 0
		if(turn == 1):
			if(game.is_over() == 2):
				trained_wins += 1
				print ("Trained Win! Score was {} to {}, running count: {} to {}".format(game.score[0,0],game.score[0,1], trained_wins, rand_wins))
			else:
				rand_wins += 1
				print("rand win. Score was {} to {}, running count: {} to {}".format(game.score[0,0],game.score[0,1], rand_wins, trained_wins))
		else:
			if(game.is_over() == 2):
				rand_wins += 1
				print("rand win. Score was {} to {}, running count: {} to {}".format(game.score[0,0],game.score[0,1], rand_wins, trained_wins))
			else:
				trained_wins += 1
				print ("Trained Win! Score was {} to {}, running count: {} to {}".format(game.score[0,0],game.score[0,1], trained_wins, rand_wins))

	print("After {} games, the agent trained for 150,000 steps has a win ratio of {} to {} against a randomly playing agent".format(num_games, trained_wins, rand_wins))
	description = "400 thousand frames made randomly, 300 thousand trained randomly, updated training net every 1000 frames"
	print(description)
	print(time_string())
	if opponent_is_random:
		opponent_is_random = False
	if(num_games - trained_wins < 10):
		player1.update_to_lead_network()
		print("updating opponent network...")
	if(num_games-trained_wins > 100):
		player1.update_to_lead_network()
		run_num = 0
		model_path = path+'/model-'+str(run_num)+'.ckpt'
		#saver.save(player2.sess, model_path)
		run_num += 1
		print("Saved Model")
		opp_name = "Random"
		s = "\n\n\n\nName of Run: {}\nName of Opponent: {}\nDescription: {}\nDate and Time of Run: {}\nWins: {}\nLosses: {}\n Model Path: {}".format(run_num, opp_name, description, time_string(), trained_wins, rand_wins, model_path)
		f = open(model_desc_file, "r")
		existing_data = f.read()
		f.close()
		f = open(model_desc_file, "w")
		f.write(existing_data+s)
		f.close()
		exit()
		