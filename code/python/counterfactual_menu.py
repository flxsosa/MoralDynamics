'''
Temporary script for running counterfactuals arbitrary
number of times for Moral Dynamics.

January 7, 2017
Felix Sosa
'''

import pymunk
import pygame
import pymunk.pygame_util
from pygame.locals import *
import sys
import simulations
import counterfactual
import helper
import csv

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
# Whether you want to write to file or not
store = True

def main():
	if store:
		# File for counterfactual results
		results_csv = open('causality.csv','w')

	# Input variable to make it work
	ALL = "ALL"

	# Print simulation menu options and record choice
	helper.printOptions()
	
	# Expected input is a tuple of integers (simulation, number of times to run it)
	choice = input()

	if (choice[0] == "ALL"):
		# Number of counterfactual simulations user wants to run
		n = choice[1]

		# Dictionary for counterfactual results
		results_dict = {}

		# While the user does not decide to exit the program
		for sim in counterfactual_menu_actions.keys():
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
				different_outcome = not(counterfactual_menu_actions[sim](space, screen, drawOptions, True))
				
				# If it did (False), increment k, otherwise (True) do not
				if different_outcome:
					k += 1
				
				# Quit the pygame instance and pygame display
				pygame.quit()
				pygame.display.quit()
			
			# Print results to user
			print "Number of different outcomes for simulation {0} was {1} out of {2}".format(sim, k, n)
			if store:
				results_dict[sim] = (k*1.0)/n
		
	else:
		# While the user does not decide to exit the program
		while (choice != '0'):
			sim = str(choice[0])
			# Number of counterfactual simulations user wants to run
			n = choice[1]
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
				boolean = counterfactual_menu_actions[sim](space, screen, drawOptions, True)
				
				# If it did (False), increment k, otherwise (True) do not
				if not boolean:
					k += 1
				
				# Quit the pygame instance and pygame display
				pygame.quit()
				pygame.display.quit()
			
			# Print results to user
			print "Number of different outcomes was {0} out of {1}".format(k, n)
			if store:
				file_results.write("{0} \t {1}".format(counterfactual_menu_actions[sim].__name__, k*1.0/n*100))
			# Inform user to make a second choice and record it
			print("Please choose a simulation or [0] to exit:")
			choice = input()
	
	# User has chosen to exit program. Say bye and exit system
	print("Goodbye")
	if store:
		# Sort the keys for the counterfactual dictionary
		keys = counterfactual_menu_actions.keys()
		keys.sort(key=int)
		
		# Create a csv writer
		writer = csv.DictWriter(results_csv, fieldnames = ['sim', 'prob'])
		
		# Write the results dictionary to a csv file
		for k in keys:
			writer.writerow({'sim':k,'prob':results_dict[k]})
		
		# Close the csv file
		results_csv.close()
	
	sys.exit()

if __name__ == '__main__':
	sys.exit(main())