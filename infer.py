'''
Infer effort of simulations and determine accuracy to ground truth.

TODO:
- Gather positional data for all bodies
- Compute Euclidean Distance for all bodies
- Score all Euclidean Distances for each guess
- Incorporate infer.py with main.py (or similar)
- Enumerate guesses with infer.py
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

def difference(sim=False, guess=False, verbose=False):
	if (guess != False and sim != False):
		# run truth simulation
		pygame.init()
		space = pymunk.Space()
		screen = pygame.display.set_mode((600,600))
		drawOptions = pymunk.pygame_util.DrawOptions(screen)
		truth = simulations.shortDistance(space,screen,drawOptions)
		pygame.quit()
		pygame.display.quit()

		# run guess simulation
		pygame.init()
		space = pymunk.Space()
		screen = pygame.display.set_mode((600,600))
		drawOptions = pymunk.pygame_util.DrawOptions(screen)
		guess = sim(space, screen, drawOptions, guess)
		pygame.quit()
		pygame.display.quit()

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
			print(eucDiffAgent[j], eucDiffPatient[j], eucDiffFireball[j])
		eucDiffTotal = sum(eucDiffAgent+eucDiffPatient+eucDiffFireball)
		print(eucDiffTotal)
def euclidean(x1, y1, x2, y2):
	return math.sqrt(pow((x1-x2),2) + pow((y1-y2),2))