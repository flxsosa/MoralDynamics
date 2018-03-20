'''
Revised main entrance into Moral Dynamics.

January 21, 2018
author: Felix Sosa
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
import argparse

# Available simulations
main_simulations = {
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
counterfactual_options = {
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

# Mode defaults to viewing original MD simulations
default_mode = 'view'

def view_simulations(args):
	'''
	View original MD simulations in pygame/pymunk

	args -- optional arguments
	'''
	# Print main simulation options and record choice
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
		main_simulations[choice](space, screen, drawOptions)
		
		# Quit the pygame instance and pygame display
		pygame.quit()
		pygame.display.quit()

		# Inform user to make a second choice and record it
		print("Please choose a simulation or [0] to exit:")
		choice = raw_input()
		
		# User has chosen to exit program. Say bye and exit system
	print("Goodbye")
	sys.exit()

def run_counterfactuals(args):
	'''
	View or run counterfactual simulations using pygame/pymunk

	args -- optional arguments
	'''
	print(args)

	# If optional arguments have been passed, parse them
	if args != None:

		# Default number of counterfactual simulations per scenario
		default_runs = 1
		choice = int(args[0])
		store_flag = bool(int(args[1]))
		
		# If 0 was passed, run through all simulations
		if choice == 0:
			# Determine if results should be stored
			if store_flag:
				# File for counterfactual results
				results_csv = open('../../data/causality.csv','w')
			
			# Number of counterfactual simulations user wants to run
			n = int(args[2]) if int(args[2]) != None else default_runs

			# Dictionary for counterfactual results
			results_dict = {}

			# While the user does not decide to exit the program
			for sim in counterfactual_options.keys():
				
				# Number of times a different outcome occurred versus the factual outcome
				k = 0

				# Run counterfactuals n times
				for i in range(n):
					# initialize pygame and create a space to contain the simulation
					pygame.init()
					space = pymunk.Space()

					# create a screen of 600x600 pixels
					screen = pygame.display.set_mode((1000,600))	
					drawOptions = pymunk.pygame_util.DrawOptions(screen)
					
					# Record whether counterfactual resulted in different outcome from factual simulation
					different_outcome = not(counterfactual_options[sim](space, screen, drawOptions, True))
					
					# If it did (False), increment k, otherwise (True) do not
					k += 1 if different_outcome else 0
					
					# Quit the pygame instance and pygame display
					pygame.quit()
					pygame.display.quit()
				
				# Print results to user
				print "Number of different outcomes for simulation {0} was {1} out of {2}".format(sim, k, n)
				if args[1]:
					results_dict[sim] = (k*1.0)/n
		
		# Else, run the chosen simulation
		else:
			# While the user does not decide to exit the program
			while (choice != 0):
				sim = str(choice)
				
				# Number of counterfactual simulations user wants to run
				n = int(args[2]) if int(args[2]) else default_runs
				
				# Number of times a different outcome occurred versus the factual outcome
				k = 0

				# Run counterfactuals n times
				for i in range(n):
					# initialize pygame and create a space to contain the simulation
					pygame.init()
					space = pymunk.Space()

					# create a screen of 600x600 pixels
					screen = pygame.display.set_mode((1000,600))	
					drawOptions = pymunk.pygame_util.DrawOptions(screen)
					
					# Record whether counterfactual resulted in different outcome from factual simulation
					different_outcome = not(counterfactual_options[sim](space, screen, drawOptions, True))
					
					# If it did (False), increment k, otherwise (True) do not
					k += 1 if different_outcome else 0
					
					# Quit the pygame instance and pygame display
					pygame.quit()
					pygame.display.quit()
				
				# Print results to user
				print "Number of different outcomes was {0} out of {1}".format(k, n)
				if store_flag:
					file_results.write("{0} \t {1}".format(counterfactual_options[sim].__name__, k*1.0/n*100))
	
	# Else, show menu and view counterfactuals
	else:
		# Print simulation menu options and record choice
		helper.printOptions()
		
		# Expected input is a tuple of integers (simulation, number of times to run it)
		choice = input()
		
		# While the user does not decide to exit the program
		while (choice != 0):
			sim = str(choice)
			
			# initialize pygame and create a space to contain the simulation
			pygame.init()
			space = pymunk.Space()

			# create a screen of 600x600 pixels
			screen = pygame.display.set_mode((1000,600))	
			drawOptions = pymunk.pygame_util.DrawOptions(screen)
			
			# Record whether counterfactual resulted in different outcome from factual simulation
			boolean = counterfactual_options[sim](space, screen, drawOptions, False)
			
			# Quit the pygame instance and pygame display
			pygame.quit()
			pygame.display.quit()
			
			# Inform user to make a second choice and record it
			print("Please choose a simulation or [0] to exit:")
			choice = input()
		
		print("Goodbye")
		sys.exit()

	if store_flag:
		# Sort the keys for the counterfactual dictionary
		keys = counterfactual_options.keys()
		keys.sort(key=int)
		
		# Create a csv writer
		writer = csv.DictWriter(results_csv, fieldnames = ['sim', 'prob'])
		
		# Write the results dictionary to a csv file
		for k in keys:
			writer.writerow({'sim':k,'prob':results_dict[k]})
		
		# Close the csv file
		results_csv.close()
	
	sys.exit()

def extract_jsons(args):
	'''
	Extract json files from MD simulations in pygame pymunk containing
	kinematic information (x,y coordinates) of each agent at each tick

	args -- optional arguments
	'''
	print(args)


def main():
	
	# AVailable modes to choose from
	options = {
		'view':view_simulations,
		'counterfactual':run_counterfactuals,
		'json':extract_jsons,
	}
	
	# Create argument parser
	parser = argparse.ArgumentParser(
		description="View simulations, run counterfactuals, or extract jsons \
		from Moral Dynamics project")

	# Add positional argument for mode and optional argument
	parser.add_argument("mode", type=str, default=default_mode,
		help="Mode of use [view, counterfactual, json]")
	parser.add_argument('--args', nargs='*',
		help="List of arbitrary arguments")

	args = parser.parse_args()
	
	# Read arguments passed and run selected mode with optional arguments
	options[args.mode](args.args)

if __name__ == '__main__':
	sys.exit(main())