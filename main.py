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
	print("=================================================")
	print("1. Short Distance")
	print("2. Medium Distance")
	print("3. Long Distance")
	print("4. Static")
	print("5. Uphill [N/A]")
	print("6. Downhill [N/A]")
	print("7. Slow Collision")
	print("8. Fast Collision")
	print("9. Dodge")
	print("10. Double Touch")
	print("11. Medium Push")
	print("12. Long Push")
	print("13. Touch")
	print("14. Push Fireball")
	print("0. EXIT")
	print("=================================================")
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
			simulations.pushFireball(space, screen, drawOptions)
		else:
			print("Must be an integer [0-14]")
		pygame.quit()
		pygame.display.quit()
		print("Please choose a Simulation [1-14] or [0] to exit:")
		choice = raw_input()
		
	print("Goodbye")
	sys.exit()
	
if __name__ == '__main__':
	sys.exit(main())