'''
Moral Dynamics

March 10, 2017

Felix Sosa

World of Cylinders, Cones, and Fireballs. 
Fireballs are harmless for Cylinders (Squares) but harmful to Cones.

Simulations to implement:

<Number>. <Factor> -- <Name> -- <Progress>

1. Distance -- Long Distance -- Complete/Edit
2. Distance -- Short Distance -- Complete/Edit
3. Distance -- Medium Distance -- Complete/Edit
4. Force/Distance -- Static Cylinder -- Complete/Edit
5. Force -- Uphill Cylinder
6. Force -- Downhill Cylinder
7. Force -- Slow Collision Cone
8. Force -- Fast Collision Cone
9. Force/Distance -- Dodging Cylinder
10. Frequency -- Double Contact Cylinder
11. Duration -- Medium Push Cylinder
12. Duration -- Long Push Cylinder
13. Duration -- Touch Cylinder - In Progress

Progress Key:
In Progress: May not be functional but working on it
Complete/Edit: Functions as needed but may need edits or optimizations
Complete: Functions and is optimal

'''

import pymunk
import pygame
import agents
import pymunk.pygame_util
from pygame.locals import *
import sys

def rem0(arbiter, space, data):
	'''
	Removes the Cone after colliding with the Fireball.
	Expected that Cone is in space.shapes[1]
	'''
	space.remove(space.shapes[1])

def longDistanceSim(space, screen, options):
	'''
	Simulation of Cylinder pushing Cone into Fireball from a long distance
	away. Originally to be compared with shortDistanceSim in Moral Kinematics.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 3: Long Distance")
	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"]=screen
	ch0.post_solve=rem0

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	
	cone = agents.patient(400, 300)
	space.add(cone.body, cone.shape)
	
	cylinder = agents.agent(100, 300)
	cylinder.set("imp", (100,0))
	space.add(cylinder.body, cylinder.shape)
	
	running = True
	while running:
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# set clock
		clock = pygame.time.Clock()
		# setup display and run sim
		screen.fill((255,255,255))
		space.step(1/50.0)
		space.debug_draw(options)
		pygame.display.flip()
		clock.tick(50)

	return

def shortDistanceSim(space, screen, options):
	'''
	Simulation of Cylinder pushing Cone into Fireball from a short distance
	away. Originally to be compared with longDistanceSim in Moral Kinematics.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 1: Short Distance")
	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"]=screen
	ch0.post_solve=rem0
	
	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	
	cone = agents.patient(400, 300)
	space.add(cone.body, cone.shape)
	
	cylinder = agents.agent(250, 300)
	cylinder.set("imp", (100,0))
	space.add(cylinder.body, cylinder.shape)

	running = True
	while running:
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# set clock
		clock = pygame.time.Clock()
		# setup display and run sim
		screen.fill((255,255,255))
		space.step(1/50.0)
		space.debug_draw(options)
		pygame.display.flip()
		clock.tick(50)

	return

def mediumDistanceSim(space, screen, options):
	'''
	Simulation of Cylinder pushing Cone into Fireball from a medium distance
	away. Originally to be compared with shortDistanceSim in Moral Kinematics.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 2: Medium Distance")
	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"]=screen
	ch0.post_solve=rem0

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	
	cone = agents.patient(400, 300)
	space.add(cone.body, cone.shape)
	
	cylinder = agents.agent(175, 300)
	cylinder.set("imp", (100,0))
	space.add(cylinder.body, cylinder.shape)

	running = True
	while running:
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# set clock
		clock = pygame.time.Clock()
		# setup display and run sim
		screen.fill((255,255,255))
		space.step(1/100.0)
		space.debug_draw(options)
		pygame.display.flip()
		clock.tick(50)

	return

def staticCylinder(space, screen, options):
	'''
	Simulation of Cone bouncing off of a static Cylinder into a Fireball.
	Originally to be compared with shortDistance in Moral Kinematics.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 4: Static Cylinder")
	# set up collision handlers
	ch0=space.add_collision_handler(0,2)
	ch0.data["surface"]=screen
	ch0.post_solve=rem0

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	
	cone = agents.patient(200, 300)
	cone.set("imp", (100,53))
	space.add(cone.body, cone.shape)
	
	cylinder = agents.agent(350, 400)
	cylinder.set("type", "s")
	space.add(cylinder.body, cylinder.shape)

	running = True
	while running:
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# set clock
		clock = pygame.time.Clock()
		# setup display and run sim
		screen.fill((255,255,255))
		space.step(1/50.0)
		space.debug_draw(options)
		pygame.display.flip()
		clock.tick(50)

	return

def main():
	'''
	Entry point
	'''
	
	# list experiment options to user
	print("Please choose a Simulation [1-13] or [0] to exit:")
	choice = raw_input()
	
	# initialize pygame and create a space to contain the simulation
	pygame.init()
	space = pymunk.Space()

	# create a screen of 600x600 pixels
	screen = pygame.display.set_mode((600,600))	
	drawOptions = pymunk.pygame_util.DrawOptions(screen)

	staticCylinder(space, screen, drawOptions)

if __name__ == '__main__':
	sys.exit(main())