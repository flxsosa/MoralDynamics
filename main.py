'''
Main file for Moral Dynamics

March 31, 2017
Felix Sosa
'''

import pymunk
import pygame
import pymunk.pygame_util
from pygame.locals import *
import sys
import simulations
import infer
import sim
import helper

menu_actions = {
	'1' : simulations.shortDistancev1,
	'2' : simulations.mediumDistancev2,
	'3' : simulations.longDistancev1,
	'4' : simulations.static,
	'5' : simulations.slowCollision,
	'6' : simulations.fastCollision,
	'7' : simulations.dodge,
	'8' : simulations.doublePush,
	'9' : simulations.mediumPush,
	'10' : simulations.longPush,
	'11' : simulations.victim_moving_static,
	'12' : simulations.noTouch,
	'13' : simulations.victim_moving_moving,
	'14' : simulations.victim_moving_static,
	'15' : simulations.victim_static_moving,
	'16' : simulations.victim_static_static,
	'17' : simulations.harm_moving_moving,
	'18' : simulations.harm_moving_static,
	'19' : simulations.harm_static_moving,
	'20' : simulations.harm_static_static,
	'21' : simulations.sim1Patient,
	'22' : simulations.sim1Fireball,
	'23' : simulations.sim2Patient,
	'24' : simulations.sim2Fireball,
	'25' : simulations.sim3Patient,
	'26' : simulations.sim3Fireball,
	'27' : simulations.sim4Patient,
	'28' : simulations.sim4Fireball,
	'29' : simulations.agentWalksToFireball,
	'30' : simulations.patientWalksToFireball,
	'31' : simulations.fireballMoving,
	'32' : simulations.agentSavesPatient
}

def main():
	'''
	Entry point
	'''

	if (len(sys.argv) == 2):
		choice = sys.argv[1]
		# initialize pygame and create a space to contain the simulation
		pygame.init()
		space = pymunk.Space()

		# create a screen of 600x600 pixels
		screen = pygame.display.set_mode((1000,600))	
		drawOptions = pymunk.pygame_util.DrawOptions(screen)
		menu_actions[choice](space, screen, drawOptions)

		pygame.quit()
		pygame.display.quit()
		sys.exit()

	helper.printHeader()
	choice = raw_input()
	# display simulation options
	if choice == '1':
		helper.printOptions()
		choice = raw_input()
		
		while (choice != '0'):
			# initialize pygame and create a space to contain the simulation
			pygame.init()
			space = pymunk.Space()

			# create a screen of 600x600 pixels
			screen = pygame.display.set_mode((1000,600))	
			drawOptions = pymunk.pygame_util.DrawOptions(screen)
			menu_actions[choice](space, screen, drawOptions)
			
			pygame.quit()
			pygame.display.quit()
			print("Please choose a simulation or [0] to exit:")
			choice = raw_input()
			
		print("Goodbye")
		sys.exit()
		
	# display guess options
	if choice == '2':
		helper.printOptions()
		choice = raw_input()
		
		while (choice != '0'):
			# create a space to contain the simulation
			space = pymunk.Space()

			# each choice executes an enumeration over a fixed interval of guess
			# impulses for each sim
			if (choice == '1'):
				infer.enum(simulations.shortDistance, 100, 300)
			elif (choice == '2'):
				infer.enum(simulations.mediumDistance, 100, 300)
			elif (choice == '3'):
				infer.enum(simulations.longDistance, 100, 300)
			elif (choice == '4'):
				infer.enum(simluations.static, 250, 450)
			elif (choice == '5'):
				simulations.uphill(space, screen, drawOptions)
			elif (choice == '6'):
				simulations.downhill(space, screen, drawOptions)
			elif (choice == '7'):
				infer.enum(simulations.slowCollision, 300, 500)
			elif (choice == '8'):
				infer.enum(simulations.fastCollision, 170, 370)
			elif (choice == '9'):
				infer.enum(simulations.dodge, 50, 250)
			elif (choice == '10'):
				infer.enum(simulations.doubleTouch, 70, 270)
			elif (choice == '11'):
				infer.enum(simulations.mediumPush, 50, 250)
			elif (choice == '12'):
				infer.enum(simulations.longPush, 10, 200)
			elif (choice == '13'):
				infer.enum(simulations.touch, 150, 350)
			elif (choice == '14'):
				infer.enum(simulations.pushFireball, 175, 375)
			else:
				print("Must be an integer [0-14]")
			pygame.quit()
			pygame.display.quit()
			print("Please choose a simulation or [0] to exit:")
			choice = raw_input()
			
		print("Goodbye")
		sys.exit()
		
if __name__ == '__main__':
	sys.exit(main())