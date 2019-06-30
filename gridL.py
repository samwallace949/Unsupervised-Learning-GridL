import numpy as np
import tensorflow as tf
import threading
import time
from gridL_agents import agent
from gridL_buffer import experience_buffer
from gridL_buffer import buffer_image
from gridL_game import gameData
def time_string():
	t = time.gmtime()
	s = ""
	s = str(t[1]) + "." + str(t[2]) + "." + str(t[0]) + "_" + str(t[3]) + ":" + str(t[4]) + ":" + str(t[5])
	return s
def max(a,b):
	if a>b:
		return a
	return b
###### ^^^^^ VARIOUS STATIC METHODS AND VARIABLES ^^^^^ ######
		
		
game = gameData(100)
b = experience_buffer(1000000)
random_player = agent(experience_buffer(1000000), game, 1)
trainables = tf.trainable_variables()
trained_player = agent(b, game, 1)
for i in range (0, 20000):
	trained_player.make_action(trained_player.get_logits(), 1-(max(i-10000, 0)/10000))
	if((i+1)%100 == 0):
		print("{} rounds completed".format(i))
	if ((i+1) % 1000 == 0 and i > 10000):
		trained_player.train(0.1, 100, 10)
game.reset_game()
rand_wins, trained_wins = 0,0
for j in range (0, 10):
	game.reset_game()
	turn,c = 0,0
	while game.is_over() == 0:
		if(i == 1):
			print (np.argmax(trained_player.get_logits()[0]))
		if(turn == 0):
			trained_player.make_action(trained_player.get_logits(), 0)
			turn = 1
		else:
			random_player.make_action(np.random.rand(1,196), 0)
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
print("After 100 games, the agent trained for 100000 steps has a win ratio of {} to {} against a randomly playing agent".format(trained_wins, rand_wins))
description = "random samples cached for ten thousand steps, then agent trains with a linear progression in its certainty of deciding the move throughout another ten thousand frames."
print(description)
print(time_string())
save_desc = input("do you want to save the results of this test? (y/n) ")
if(save_desc == "y"):
	run_name = input("Name of Run: ")
	opp_name = input("Name of Opponent: ")
	s = "Name of Run: {}\nName of Opponent: {}\nDescription: {}\nDate and Time of Run: {}\nWins: {}\nLosses: {}\n".format(run_name, opp_name, description, time_string(), trained_wins, rand_wins)
