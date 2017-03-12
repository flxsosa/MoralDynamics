'''
Moral Dynamics

March 10, 2017

World of Cylinders, Cones, and Fireballs. 
Fireballs are harmless for Cylinders (Squares) but harmful to Cones.

Simulations to implement:

<Number>. <Factor> -- <Name> -- <Progress>

1. Distance -- Long Distance -- In Progress
2. Distance -- Short Distance -- In Progress
3. Distance -- Medium Distance
4. Force/Distance -- Static Cylinder
5. Force -- Uphill Cylinder
6. Force -- Downhill Cylinder
7. Force -- Slow Collision Cone
8. Force -- Fast Collision Cone
9. Force/Distance -- Dodging Cylinder
10. Frequency -- Double Contact Cylinder
11. Duration -- Medium Push Cylinder
12. Duration -- Long Push Cylinder
13. Duration -- Touch Cylinder

Experiments to implement:

...

'''

import pymunk
import pygame
import pymunk.pygame_util
from pygame.locals import *
import sys

def addCone(space,x,y):
	'''
	Addsa a cone to the simulation at a given position.
	space -- pymunk simulation space
	x -- x coordinate
	y -- y coordinate
	'''
	body = pymunk.Body(1,1)
	body.position = x,y
	shape = pymunk.Poly(body, [(0, 20),(20, -20),(-20, -20)])
	space.add(shape)
	return shape

def addCylinder(space, x, y):
	'''
	Adds a cylinder [square] to teh simulation at a given position.
	space -- pymunk simulation space
	x -- x coordinate
	y -- y coordinate
	'''
	body = pymunk.Body(1,1)
	body.position = x,y
	shape = pymunk.Poly.create_box(body, (30,30))
	space.add(body,shape)
	return shape

def addFireball(space, x, y, rad=15):
	'''
	Adds a fireball to the simulation at a given position.
	space -- pymunk simulation space
	x -- x coordinate
	y -- y coordinate
	rad -- circle radius
	'''
	body = pymunk.Body(body_type=pymunk.Body.STATIC)
	body.position = x,y # 3
	shape = pymunk.Circle(body, rad)
	shape.color = pygame.color.THECOLORS["red"]
	space.add(body,shape) # 5
	return shape

def longDistanceSim(space, screen, options):
	'''
	Simulation of Cylinder pushing Cone into Fireball from a long distance
	away. Originally to be compared with shortDistanceSim in Moral Kinematics.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''

	while True:
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				sys.exit(0)

		# set clock
		clock = pygame.time.Clock()

		# add shapes
		ball = addFireball(space, 500, 300)
		cone = addCone(space, 400, 300)
		cylinder = addCylinder(space, 100, 300)

		# setup display and run sim
		screen.fill((255,255,255))
		space.step(1/50.0)
		space.debug_draw(options)
		pygame.display.flip()
		pygame.display.set_caption("Simulation 1: Long Distance")
		clock.tick(50)

def shortDistanceSim(space, screen, options):
	'''
	Simulation of Cylinder pushing Cone into Fireball from a short distance
	away. Originally to be compared with longDistanceSim in Moral Kinematics.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''

	while True:
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				sys.exit(0)

		# set clock
		clock = pygame.time.Clock()

		# add shapes
		ball = addFireball(space, 400, 300)
		cone = addCone(space, 300, 300)
		cylinder = addCylinder(space, 150, 300)

		# setup display and run sim
		screen.fill((255,255,255))
		space.step(1/50.0)
		space.debug_draw(options)
		pygame.display.flip()
		pygame.display.set_caption("Simulation 2: Short Distance")
		clock.tick(50)

def main():
	'''
	Entry point
	'''
	
	# list experiment options to user
	print("Please choose a Simulation [1-13]:")
	choice = raw_input()

	# initialize pygame and create a space to contain the simulation
	pygame.init()
	space = pymunk.Space()

	# create a screen of 600x600 pixels
	screen = pygame.display.set_mode((600,600))	
	drawOptions = pymunk.pygame_util.DrawOptions(screen)
	
	#longDistanceSim(space, screen, drawOptions)
	shortDistanceSim(space, screen, drawOptions)

if __name__ == '__main__':
	sys.exit(main())