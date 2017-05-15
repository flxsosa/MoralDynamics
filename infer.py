'''
Infer effort of simulations and determine accuracy to ground truth.

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

class infer:
	'''
	A class for inferring effort
	'''
	def __init__(self, guess, sim):
		'''
		guess -- initital guess of effort at each timestep
		sim - list of sims to be simulated
		'''
		self.guess = guess
		self.sim = sim
		self.score = None

	def difference(self, verbose=False):
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
		guess = simulations.shortDistance(space, screen, drawOptions, self.guess)
		pygame.quit()
		pygame.display.quit()

		xDiff =[]
		yDiff =[]
		eucDiff=[]
		for j in range(len(truth[0])):
			xDiff.append(math.fabs(truth[0][j]-guess[0][j]))
			yDiff.append(math.fabs(truth[1][j]-guess[1][j]))
			e = euclidean(truth[0][j], truth[1][j], guess[0][j], guess[1][j])
			eucDiff.append(e)

		print("Step \t Truth \t Guess \t xDiff \t yDiff \t EucDiff")
		if (verbose):
			for i in range(len(truth)):
				print i, '\t', truth[i], '\t', guess[i], '\t', xDiff[i], '\t', yDiff[i], '\t', eucDiff[i]

		print "X \t X \t X \t", sum(xDiff), " \t ", sum(yDiff), " \t ", sum(eucDiff)

def euclidean(x1, y1, x2, y2):
	return math.sqrt(pow((x1-x2),2)+pow((y1-y2),2))