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
import convert_to_blender

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
		
if __name__ == '__main__':
	sys.exit(main())