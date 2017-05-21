'''
Infer effort of simulations and determine accuracy to ground truth.

TODO:
x Gather positional data for all bodies
x Compute Euclidean Distance for all bodies
- Score all Euclidean Distances for each guess
- Incorporate infer.py with main.py (or similar)
x Enumerate guesses with infer.py
- Modify all sims to work with infer.py

May 12, 2017
Felix Sosa 
'''


import pymunk
import pygame
import agents
import pymunk.pygame_util
from pygame.locals import *
import sys
import simulations
import math
import matplotlib.pyplot as plt

def enum(sim, low, high):
	min = (10000000,0)
	bestList = []
	for i in range(low,high,10):
		print "Impulse: ", i
		best = difference(sim, i)
		bestList.append(best)
		if best[0] < min[0]:
			min = best
		print "Best guess so far is ", min[1]
	print "Best guess is ", min[1]
	plot(bestList)

def difference(sim=False, imp=False, verbose=False):
	if (imp != False and sim != False):
		# run truth simulation
		print "Impulse: ", imp
		pygame.init()
		space = pymunk.Space()
		screen = None # pygame.display.set_mode((600,600))
		drawOptions = None #pymunk.pygame_util.DrawOptions(screen)
		truth = simulations.shortDistance(space,screen,drawOptions)
		pygame.quit()
		#pygame.display.quit()

		# run guess simulation
		pygame.init()
		space = pymunk.Space()
		#screen = pygame.display.set_mode((600,600))
		#drawOptions = pymunk.pygame_util.DrawOptions(screen)
		guess = sim(space, screen, drawOptions, imp)
		pygame.quit()
		#pygame.display.quit()

		# declare lists for euclidean distances for each body
		eucDiffAgent = []
		eucDiffPatient = []
		eucDiffFireball = []
		eucDiffTotal = []

		for j in range(len(truth[0])):
			# gather euclidean distances between truth and guess for each body at each timestep
			eucDiffAgent.append(euclidean(truth[0][j], truth[1][j], guess[0][j], guess[1][j]))
			eucDiffPatient.append(euclidean(truth[2][j], truth[3][j], guess[2][j], guess[3][j]))
			eucDiffFireball.append(euclidean(truth[4][j], truth[5][j], guess[4][j], guess[5][j]))
			#print(eucDiffAgent[j], eucDiffPatient[j], eucDiffFireball[j])
		eucDiffTotal = sum(eucDiffAgent+eucDiffPatient+eucDiffFireball)
		print "Total Distance: ", eucDiffTotal
		return (eucDiffTotal, imp)

def euclidean(x1, y1, x2, y2):
	return math.sqrt(pow((x1-x2),2) + pow((y1-y2),2))

def plot(list):
	x = []
	y = []
	for item in list:
		x.append(item[1])
		y.append(item[0])
	print x
	print y
	plt.bar(x, y)
	plt.show()