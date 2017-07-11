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
import infer
import sim
import matplotlib.pyplot as plt
import helper

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

		if (choice == '1'):
			simulations.shortDistancev1(space, screen, drawOptions)
		elif (choice == '2'):
			simulations.mediumDistancev2(space, screen, drawOptions)
		elif (choice == '3'):
			simulations.longDistancev1(space, screen, drawOptions)
		elif (choice == '4'):
			simulations.longDistancev2(space, screen, drawOptions)
		elif (choice == '5'):
			simulations.static(space, screen, drawOptions)
		elif (choice == '6'):
			simulations.slowCollision(space, screen, drawOptions)
		elif (choice == '7'):
			simulations.fastCollision(space, screen, drawOptions)
		elif (choice == '8'):
			simulations.dodge(space, screen, drawOptions)
		elif (choice == '9'):
			simulations.doublePush(space, screen, drawOptions)
		elif (choice == '10'):
			simulations.mediumPush(space, screen, drawOptions)
		elif (choice == '11'):
			simulations.longPush(space, screen, drawOptions)
		elif (choice == '13'):
			simulations.noTouch(space, screen, drawOptions)

		elif (choice == '14'):
			simulations.victim_moving_moving(space, screen, drawOptions)
		elif (choice == '15' or choice == '12'):
			simulations.victim_moving_static(space, screen, drawOptions)
		elif (choice == '16'):
			simulations.victim_static_moving(space, screen, drawOptions)
		elif (choice == '17'):
			simulations.victim_static_static(space, screen, drawOptions)
		elif (choice == '18'):
			simulations.harm_moving_moving(space, screen, drawOptions)
		elif (choice == '19'):
			simulations.harm_moving_static(space, screen, drawOptions)
		elif (choice == '20'):
			simulations.harm_static_moving(space, screen, drawOptions)
		elif (choice == '21'):
			simulations.harm_static_static(space, screen, drawOptions)
		
		elif (choice == '22'):
			simulations.sim1Patient(space, screen, drawOptions)
		elif (choice == '23'):
			simulations.pushFireball(space, screen, drawOptions)

		elif (choice == '24'):
			simulations.agentWalksToFireball(space, screen, drawOptions)
		elif (choice == '25'):
			simulations.patientWalksToFireball(space, screen, drawOptions)
		elif (choice == '26'):
			simulations.fireballMoving(space, screen, drawOptions)
		elif (choice == '27'):
			simulations.agentSavesPatient(space, screen, drawOptions)
		else:
			print("Must be an integer [0-14]")
		pygame.quit()
		pygame.display.quit()
		sys.exit()

	print("=================================================")
	print("1. Show Simulations")
	print("2. Run Guesses")
	print("0. EXIT")
	print("=================================================")
	print("Please choose an option or [0] to exit:")
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

			if (choice == '1'):
				simulations.shortDistancev1(space, screen, drawOptions)
			elif (choice == '2'):
				simulations.mediumDistancev2(space, screen, drawOptions)
			elif (choice == '3'):
				simulations.longDistancev1(space, screen, drawOptions)
			elif (choice == '4'):
				simulations.longDistancev2(space, screen, drawOptions)
			elif (choice == '5'):
				simulations.static(space, screen, drawOptions)
			elif (choice == '6'):
				simulations.slowCollision(space, screen, drawOptions)
			elif (choice == '7'):
				simulations.fastCollision(space, screen, drawOptions)
			elif (choice == '8'):
				simulations.dodge(space, screen, drawOptions)
			elif (choice == '9'):
				simulations.doublePush(space, screen, drawOptions)
			elif (choice == '10'):
				simulations.mediumPush(space, screen, drawOptions)
			elif (choice == '11'):
				simulations.longPush(space, screen, drawOptions)
			elif (choice == '13'):
				simulations.noTouch(space, screen, drawOptions)

			elif (choice == '14'):
				simulations.victim_moving_moving(space, screen, drawOptions)
			elif (choice == '15' or choice == '12'):
				simulations.victim_moving_static(space, screen, drawOptions)
			elif (choice == '16'):
				simulations.victim_static_moving(space, screen, drawOptions)
			elif (choice == '17'):
				simulations.victim_static_static(space, screen, drawOptions)
			elif (choice == '18'):
				simulations.harm_moving_moving(space, screen, drawOptions)
			elif (choice == '19'):
				simulations.harm_moving_static(space, screen, drawOptions)
			elif (choice == '20'):
				simulations.harm_static_moving(space, screen, drawOptions)
			elif (choice == '21'):
				simulations.harm_static_static(space, screen, drawOptions)
			
			elif (choice == '22'):
				simulations.sim1Patient(space, screen, drawOptions)
			elif (choice == '23'):
				simulations.sim1Fireball(space, screen, drawOptions)
			elif (choice == '24'):
				simulations.sim2Patient(space, screen, drawOptions)
			elif (choice == '25'):
				simulations.sim2Fireball(space, screen, drawOptions)
			elif (choice == '26'):
				simulations.sim3Patient(space, screen, drawOptions)
			elif (choice == '27'):
				simulations.sim3Fireball(space, screen, drawOptions)

			elif (choice == '28'):
				simulations.agentWalksToFireball(space, screen, drawOptions)
			elif (choice == '29'):
				simulations.patientWalksToFireball(space, screen, drawOptions)
			elif (choice == '30'):
				simulations.fireballMoving(space, screen, drawOptions)
			elif (choice == '31'):
				simulations.agentSavesPatient(space, screen, drawOptions)
			else:
				print("Must be an integer [0-14]")
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