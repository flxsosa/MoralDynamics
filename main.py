'''
Moral Dynamics

March 31, 2017

Felix Sosa

World of Cylinders, Cones, and Fireballs. 
Fireballs are harmless for Cylinders (Squares) but harmful to Cones.

Main file
'''

import pymunk
import pygame
import agents
import pymunk.pygame_util
from pygame.locals import *
import sys
import simulations

def main():
	'''
	Entry point
	'''
	
	# list experiment options to user
	print("Please choose a Simulation [1-13] or [0] to exit:")
	choice = raw_input()
	
	# initialize pygame and create a space to contain the simulation
	pygame.init()
	space = pymunk.Space()

	# create a screen of 600x600 pixels
	screen = pygame.display.set_mode((600,600))	
	drawOptions = pymunk.pygame_util.DrawOptions(screen)

	simulations.test(space, screen, drawOptions)

if __name__ == '__main__':
	sys.exit(main())