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
import counterfactual
import sim
import helper
import convert_to_blender

# Available simulations
simulation_menu_actions = {
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
	'32' : simulations.agent_saves_patient
}

# Available counterfactuals
counterfactual_menu_actions = {
	'1' : counterfactual.short_distance_v1,
	'2' : counterfactual.medium_distance_v2,
	'3' : counterfactual.long_distance_v1,
	'4' : counterfactual.static,
	'5' : counterfactual.slow_collision,
	'6' : counterfactual.fast_collision,
	'7' : counterfactual.dodge,
	'8' : counterfactual.double_push,
	'9' : counterfactual.medium_push,
	'10' : counterfactual.long_push,
	'11' : counterfactual.victim_moving_static,
	'12' : counterfactual.no_touch,
	'13' : counterfactual.victim_moving_moving,
	'14' : counterfactual.victim_moving_static,
	'15' : counterfactual.victim_static_moving,
	'16' : counterfactual.victim_static_static,
	'17' : counterfactual.harm_moving_moving,
	'18' : counterfactual.harm_moving_static,
	'19' : counterfactual.harm_static_moving,
	'20' : counterfactual.harm_static_static,
	'21' : counterfactual.sim_1_patient,
	'22' : counterfactual.sim_1_fireball,
	'23' : counterfactual.sim_2_patient,
	'24' : counterfactual.sim_2_fireball,
	'25' : counterfactual.sim_3_patient,
	'26' : counterfactual.sim_3_fireball,
	'27' : counterfactual.sim_4_patient,
	'28' : counterfactual.sim_4_fireball
}

convert_to_blender_menu_actions = {
	'1' : convert_to_blender.short_distance_v1,
	'2' : convert_to_blender.medium_distance_v2,
	'3' : convert_to_blender.long_distance_v1,
	'4' : convert_to_blender.static,
	'5' : convert_to_blender.slow_collision,
	'6' : convert_to_blender.fast_collision,
	'7' : convert_to_blender.dodge,
	'8' : convert_to_blender.double_push,
	'9' : convert_to_blender.medium_push,
	'10' : convert_to_blender.long_push,
	'11' : convert_to_blender.victim_moving_static,
	'12' : convert_to_blender.no_touch,
	'13' : convert_to_blender.victim_moving_moving,
	'14' : convert_to_blender.victim_moving_static,
	'15' : convert_to_blender.victim_static_moving,
	'16' : convert_to_blender.victim_static_static,
	'17' : convert_to_blender.harm_moving_moving,
	'18' : convert_to_blender.harm_moving_static,
	'19' : convert_to_blender.harm_static_moving,
	'20' : convert_to_blender.harm_static_static,
	'21' : convert_to_blender.sim_1_patient,
	'22' : convert_to_blender.sim_1_fireball,
	'23' : convert_to_blender.sim_2_patient,
	'24' : convert_to_blender.sim_2_fireball,
	'25' : convert_to_blender.sim_3_patient,
	'26' : convert_to_blender.sim_3_fireball,
	'27' : convert_to_blender.sim_4_patient,
	'28' : convert_to_blender.sim_4_fireball,
	'29' : convert_to_blender.agent_walks_to_fireball,
	'30' : convert_to_blender.patient_walks_to_fireball,
	'31' : convert_to_blender.fireball_moving,
	'32' : convert_to_blender.agent_saves_patient
}

def main():
	'''
	Entry point
	'''

	# If
	if (len(sys.argv) == 2):
		choice = sys.argv[1]
		# initialize pygame and create a space to contain the simulation
		pygame.init()
		space = pymunk.Space()

		# create a screen of 600x600 pixels
		screen = pygame.display.set_mode((1000,600))	
		drawOptions = pymunk.pygame_util.DrawOptions(screen)
		# In converting to blender we don't want the pygame display to show
		convert_to_blender_menu_actions[choice](space, None, None)

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
			simulation_menu_actions[choice](space, screen, drawOptions)
			
			# Quit the pygame instance and pygame display
			pygame.quit()
			pygame.display.quit()

			# Inform user to make a second choice and record it
			print("Please choose a simulation or [0] to exit:")
			choice = raw_input()
		
		# User has chosen to exit program. Say bye and exit system
		print("Goodbye")
		sys.exit()
		
	# If user chooses, display counterfactual menu options
	if choice == '2':
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
			counterfactual_menu_actions[choice](space, screen, drawOptions)
			
			# Quit the pygame instance and pygame display
			pygame.quit()
			pygame.display.quit()

			# Inform user to make a second choice and record it
			print("Please choose a simulation or [0] to exit:")
			choice = raw_input()
		
		# User has chosen to exit program. Say bye and exit system
		print("Goodbye")
		sys.exit()

	# If user chooses, display counterfactual menu options
	if choice == '3':
		choice = raw_input()
		
		# While the user does not decide to exit the program
		while (choice != '0'):
			# initialize pygame and create a space to contain the simulation
			pygame.init()
			space = pymunk.Space()

			# create a screen of 600x600 pixels
			screen = pygame.display.set_mode((1000,600))	
			drawOptions = pymunk.pygame_util.DrawOptions(screen)
			convert_to_blender.long_distance_v1(space, screen, drawOptions)
			
			# Quit the pygame instance and pygame display
			pygame.quit()
			pygame.display.quit()

			# Inform user to make a second choice and record it
			print("Please choose a simulation or [0] to exit:")
			choice = raw_input()
		
		# User has chosen to exit program. Say bye and exit system
		print("Goodbye")
		sys.exit()

	# If user chooses, display simulation menu options
	if choice == '4':
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
			convert_to_blender_menu_actions[choice](space, screen, drawOptions)
			
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