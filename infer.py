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

	def simulate(self):
		for s in self.sim:
			pygame.init()
			space = pymunk.Space()
			screen = pygame.display.set_mode((600,600))
			drawOptions = pymunk.pygame_util.DrawOptions(screen)

			simulations.shortDistance(space, screen, drawOptions, self.guess)
		

	def difference(self):
		pass