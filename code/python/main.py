'''
Main file for Moral Dynamics

March 31, 2017
Felix Sosa
'''

'''
Main file for Moral Dynamics project.

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

# Available simulations
menu_actions = {
	'1' : simulations.short_distance_v1,
	'2' : simulations.medium_distance_v2,
	'3' : simulations.long_distance_v1,
	'4' : simulations.static,
	'5' : simulations.slow_collision,
	'6' : simulations.fast_collision,
	'7' : simulations.dodge,
	'8' : simulations.double_push,
	'9' : simulations.medium_push,
	'10' : simulations.long_push,
	'11' : simulations.victim_moving_static,
	'12' : simulations.no_touch,
	'13' : simulations.victim_moving_moving,
	'14' : simulations.victim_moving_static,
	'15' : simulations.victim_static_moving,
	'16' : simulations.victim_static_static,
	'17' : simulations.harm_moving_moving,
	'18' : simulations.harm_moving_static,
	'19' : simulations.harm_static_moving,
	'20' : simulations.harm_static_static,
	'21' : simulations.sim_1_patient,
	'22' : simulations.sim_1_fireball,
	'23' : simulations.sim_2_patient,
	'24' : simulations.sim_2_fireball,
	'25' : simulations.sim_3_patient,
	'26' : simulations.sim_3_fireball,
	'27' : simulations.sim_4_patient,
	'28' : simulations.sim_4_fireball,
	'29' : simulations.agent_walks_to_fireball,
	'30' : simulations.patient_walks_to_fireball,
	'31' : simulations.fireball_moving,
	'32' : simulations.agent_saves_patient,
	'c' : simulations.counterfactual_short_distance
}

def main():
	'''
	Entry point
	'''

	# If user supplies simulation choice at launch
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

	# Print main menu options to user otherwise and record choice
	helper.printHeader()
	choice = raw_input()
	
	# If user chooses, display simulation menu options
	if choice == '1':
		# Print simulation menu options and record choice
		helper.printOptions()
		choice = raw_input()
		
		# While the user does not decide to exit the program
		while (choice != '0'):
			# initialize pygame and create a space to contain the simulation
			pygame.init()
			space = pymunk.Space()

			# create a screen of 600x600 pixels
			screen = pygame.display.set_mode((1000,600))	
			drawOptions = pymunk.pygame_util.DrawOptions(screen)
			menu_actions[choice](space, screen, drawOptions)
			
			# Quit the pygame instance and pygame display
			pygame.quit()
			pygame.display.quit()

			# Inform user to make a second choice and record it
			print("Please choose a simulation or [0] to exit:")
			choice = raw_input()
		
		# User has chosen to exit program. Say bye and exit system
		print("Goodbye")
		sys.exit()
		
	# If user chooses, display guess menu options
	if choice == '2':
		# Print simulation menu options and record choice
		helper.printOptions()
		choice = raw_input()
		
		# While the user does not decide to exit the program
		while (choice != '0'):
			# Create a pymunk space instance to contain the simulation
			space = pymunk.Space()

			# Each choice executes an enumeration over a fixed interval of guess
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
			
			# Quit the pygame instance and pygame display
			pygame.quit()
			pygame.display.quit()

			# Inform user to make a second choice and record it
			print("Please choose a simulation or [0] to exit:")
			choice = raw_input()
		
		# User has chosen to exit program. Say bye and exit system
		print("Goodbye")
		sys.exit()
		
if __name__ == '__main__':
	sys.exit(main())