'''
Infer effort of simulations and determine accuracy to ground truth.

TODO:
x Gather positional data for all bodies
x Compute Euclidean Distance for all bodies
- Score all Euclidean Distances for each guess
x Incorporate infer.py with main.py (or similar)
x Enumerate guesses with infer.py
- Modify all sims to work with infer.py

May 12, 2017
Felix Sosa
'''


import pymunk
import pygame
import agents
import math
from pygame.locals import *
import matplotlib.pyplot as plt

def enum(sim, low, high):
	'''
	Enumerate over a fixed interval of impulses for a given sim.
	sim -- simulation to be enumerated
	low -- lower bound of impulse interval
	high -- upper bound of impulse interval
	'''
	min = best = difference(sim, low)
	bestList = [best]
	for i in range(low+10,high+10,10):
		print "Impulse: ", i
		best = difference(sim, i)
		bestList.append(best)
		if best[0] < min[0]:
			min = best
		#print "Best guess so far is ", min[1]
	print "Best guess is ", min[1]
	plot(bestList)

def difference(sim=False, imp=False):
	'''
	Find the euclidean distance of the agent, patient, and
	fireball between a truth simulation and a guess simulation.
	sim -- the simulation to be compared
	imp -- the guess impulse for the guess simulation
	'''
	# check if sim and impulse parameters were passed
	if (imp != False and sim != False):
		# run truth simulation
		print "Impulse: ", imp
		pygame.init()
		space = pymunk.Space()
		truth = sim(space,None,None, True)
		pygame.quit()
		# run guess simulation
		pygame.init()
		space = pymunk.Space()
		guess = sim(space, None, None, True, imp)
		pygame.quit()
		# declare lists for euclidean distances for each body
		eucDiffAgent = []
		eucDiffPatient = []
		eucDiffFireball = []
		eucDiffTotal = []
		# gather euclidean distances between truth and guess for each body at each timestep
		for j in range(len(truth[0])):
			eucDiffAgent.append(euclidean(truth[0][j], truth[1][j], guess[0][j], guess[1][j]))
			eucDiffPatient.append(euclidean(truth[2][j], truth[3][j], guess[2][j], guess[3][j]))
			eucDiffFireball.append(euclidean(truth[4][j], truth[5][j], guess[4][j], guess[5][j]))

		eucDiffTotal = sum(eucDiffAgent+eucDiffPatient+eucDiffFireball)
		print "Total Distance: ", eucDiffTotal
		return (eucDiffTotal, imp)

def euclidean(x1, y1, x2, y2):
	'''
	Calculate 2D euclidean distance.
	'''
	return math.sqrt(pow((x1-x2),2) + pow((y1-y2),2))

def plot(list):
	'''
	Create a bar graph using pyplot given x and y axis
	data.
	list -- list of (y,x) tuples
	'''
	x = []
	y = []
	# traverse list and create x and y axis lists
	for item in list:
		x.append(item[1])
		y.append(item[0])
	# create bar graph object and display it
	plt.bar(x, y)
	plt.show()