'''
Moral Dynamics

March 10, 2017

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
13. Duration -- Touch Cylinder

Progress Key:
In Progress: May not be functional but working on it
Complete/Edit: Functions as needed but may need edits or optimizations
Complete: Functions and is optimal

'''

import pymunk
import pygame
import pymunk.pygame_util
from pygame.locals import *
import sys

def rem0(arbiter, space, data):
	'''
	Removes the Cone after colliding with the Fireball.
	Expected that Cone is in space.shapes[1]
	'''
	space.remove(space.shapes[1])

def rem1(arbiter, space, data):
	'''
	Stops Cylinder after colliding with Cone and applies (guestimated)
	impulse to Cone. Expected that Cone is in shapes[1] and Cylinder 
	is in shapes[2]
	'''
	space.shapes[2].body.velocity = (0,0)
	space.shapes[1].body.apply_impulse_at_local_point((100,0))

def addCone(space,x,y, imp=(0,0)):
	'''
	Adds a a [green cylinder] to the simulation at a given position.
	space -- pymunk simulation space
	x -- x coordinate
	y -- y coordinate
	'''
	body = pymunk.Body(1,1)
	body.position = x,y
	body.apply_impulse_at_local_point(imp)
	shape = pymunk.Poly(body, [(0, 20),(20, -20),(-20, -20)])
	shape.collision_type = 0
	shape.elasticity = 1
	space.add(body, shape)
	return shape

def addCylinder(space, x, y, imp=(0,0), flag=True):
	'''
	Adds a cylinder [square] to teh simulation at a given position.
	space -- pymunk simulation space
	x -- x coordinate
	y -- y coordinate
	imp -- impulse for the cylinder
	'''
	if flag:
		body = pymunk.Body(10,1, body_type=pymunk.Body.DYNAMIC)
	else:
		body = pymunk.Body(body_type=pymunk.Body.STATIC)
	body.position = x,y
	body.apply_impulse_at_local_point(imp)
	shape = pymunk.Poly.create_box(body, (30,30))
	shape.collision_type = 1
	shape.elasticity = 1
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
	body.position = x,y 
	shape = pymunk.Circle(body, rad)
	shape.color = pygame.color.THECOLORS["red"]
	shape.collision_type = 2
	space.add(body,shape) 
	return shape

def longDistanceSim(space, screen, options):
	'''
	Simulation of Cylinder pushing Cone into Fireball from a long distance
	away. Originally to be compared with shortDistanceSim in Moral Kinematics.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 1: Long Distance")
	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"]=screen
	ch0.post_solve=rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"]=screen
	ch1.post_solve=rem1

	# add shapes
	ball = addFireball(space, 500, 300)
	cone = addCone(space, 400, 300)
	cylinder = addCylinder(space, 100, 300, (1000,0))

	while True:
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				sys.exit(0)

		# set clock
		clock = pygame.time.Clock()
		# setup display and run sim
		screen.fill((255,255,255))
		space.step(1/50.0)
		space.debug_draw(options)
		pygame.display.flip()
		clock.tick(50)

def shortDistanceSim(space, screen, options):
	'''
	Simulation of Cylinder pushing Cone into Fireball from a short distance
	away. Originally to be compared with longDistanceSim in Moral Kinematics.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 2: Short Distance")
	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"]=screen
	ch0.post_solve=rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"]=screen
	ch1.post_solve=rem1

	# add shapes
	ball = addFireball(space, 500, 300)
	cone = addCone(space, 400, 300)
	cylinder = addCylinder(space, 250, 300, (1000,0))

	while True:
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				sys.exit(0)

		# set clock
		clock = pygame.time.Clock()

		# setup display and run sim
		screen.fill((255,255,255))
		space.step(1/50.0)
		space.debug_draw(options)
		pygame.display.flip()
		clock.tick(50)

def mediumDistanceSim(space, screen, options):
	'''
	Simulation of Cylinder pushing Cone into Fireball from a medium distance
	away. Originally to be compared with shortDistanceSim in Moral Kinematics.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 3: Medium Distance")
	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"]=screen
	ch0.post_solve=rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"]=screen
	ch1.post_solve=rem1

	# add shapes
	ball = addFireball(space, 500, 300)
	cone = addCone(space, 400, 300)
	cylinder = addCylinder(space, 175, 300, (1000,0))

	while True:
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				sys.exit(0)

		# set clock
		clock = pygame.time.Clock()
		# setup display and run sim
		screen.fill((255,255,255))
		space.step(1/50.0)
		space.debug_draw(options)
		pygame.display.flip()
		clock.tick(50)

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
	ball = addFireball(space, 500, 300)
	cone = addCone(space, 200, 300, (100,55))
	cylinder = addCylinder(space, 350, 400, (0,0), False)

	while True:
		# allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				sys.exit(0)

		# setup display and run sim
		clock = pygame.time.Clock()
		screen.fill((255,255,255))
		space.step(1/50.0)
		space.debug_draw(options)
		pygame.display.flip()
		clock.tick(50)

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