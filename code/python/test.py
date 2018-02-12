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
import exp2_simulations
import exp2_counterfactuals

good_counterfactual_menu = {
	'1' : exp2_counterfactuals.good_1,
	'2' : exp2_counterfactuals.good_2,
	'3' :exp2_counterfactuals.good_3,
	'4' :exp2_counterfactuals.good_4,
	'5' :exp2_counterfactuals.good_5,
	'6' :exp2_counterfactuals.good_6,
	'7' :exp2_counterfactuals.good_7,
	'8' :exp2_counterfactuals.good_8,
	'9' :exp2_counterfactuals.good_9,
	'10' :exp2_counterfactuals.good_10,
	'11' :exp2_counterfactuals.good_11,
	'12' :exp2_counterfactuals.good_12,
	'13' :exp2_counterfactuals.short_distance_fireball,
	'14' :exp2_counterfactuals.short_distance_patient,
	'15' :exp2_counterfactuals.sim_2_fireball,
	'16' :exp2_counterfactuals.sim_2_patient,
	'17' :exp2_counterfactuals.no_touch_fireball,
	'18' :exp2_counterfactuals.no_touch_patient,
	'19' :exp2_counterfactuals.sim_1_fireball,
	'20' :exp2_counterfactuals.sim_1_patient,
	'21' :exp2_counterfactuals.static_fireball,
	'22' :exp2_counterfactuals.static_patient,
	'23' :exp2_counterfactuals.bump_fireball,
	'24' :exp2_counterfactuals.bump_patient
}

def main():
	'''
	Entry point
	'''

	# If
	if (len(sys.argv) == 2):
		
		for key in good_counterfactual_menu.keys():
			choice = key
			# initialize pygame and create a space to contain the simulation
			# pygame.init()
			space = pymunk.Space()
			print "Simulation {0}".format(key)
			# create a screen of 600x600 pixels
			# screen = pygame.display.set_mode((1000,600))	
			# drawOptions = pymunk.pygame_util.DrawOptions(screen)
			# In converting to blender we don't want the pygame display to show
			good_counterfactual_menu[choice](space, None, None, True)

			# pygame.quit()
			# pygame.display.quit()
		sys.exit()

if __name__ == '__main__':
	sys.exit(main())