'''
Main file for Moral Dynamics

March 31, 2017
Felix Sosa
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
	
	while (choice != '0'):
		# initialize pygame and create a space to contain the simulation
		pygame.init()
		space = pymunk.Space()

		# create a screen of 600x600 pixels
		screen = pygame.display.set_mode((600,600))	
		drawOptions = pymunk.pygame_util.DrawOptions(screen)

		if (choice == '1'):
			simulations.shortDistance(space, screen, drawOptions)
		elif (choice == '2'):
			simulations.mediumDistance(space, screen, drawOptions)
		elif (choice == '3'):
			simulations.longDistance(space, screen, drawOptions)
		elif (choice == '4'):
			simulations.static(space, screen, drawOptions)
		elif (choice == '5'):
			simulations.uphill(space, screen, drawOptions)
		elif (choice == '6'):
			simulations.downhill(space, screen, drawOptions)
		elif (choice == '7'):
			simulations.slowCollision(space, screen, drawOptions)
		elif (choice == '8'):
			simulations.fastCollision(space, screen, drawOptions)
		elif (choice == '9'):
			simulations.dodge(space, screen, drawOptions)
		elif (choice == '10'):
			simulations.doubleTouch(space, screen, drawOptions)
		elif (choice == '11'):
			simulations.mediumPush(space, screen, drawOptions)
		elif (choice == '12'):
			simulations.longPush(space, screen, drawOptions)
		elif (choice == '13'):
			simulations.touch(space, screen, drawOptions)
		elif (choice == '14'):
			simulations.test(space, screen, drawOptions)

		pygame.quit()
		pygame.display.quit()
		print("Please choose a Simulation [1-13] or [0] to exit:")
		choice = raw_input()
		
	print("Goodbye")
	sys.exit()
	
if __name__ == '__main__':
	sys.exit(main())