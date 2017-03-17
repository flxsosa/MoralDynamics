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
7. Force -- Slow Collision Cone - Complete/Edit
8. Force -- Fast Collision Cone - Complete/Edit
9. Force/Distance -- Dodging Cylinder - Complete/Editgit m
10. Frequency -- Double Contact Cylinder - Complete/Edit
11. Duration -- Medium Push Cylinder - Complete/Edit
12. Duration -- Long Push Cylinder - Complete/Edit
13. Duration -- Touch Cylinder - Complete/Edit

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

def rem1(arbiter, space, data):
	'''
	Causes cone to travel slower after being hit by Cylinder.
	'''
	space.shapes[1].body.velocity = \
	(space.shapes[1].body.velocity[0]/2.5, 
		space.shapes[1].body.velocity[1]/2.5)
	space.shapes[2].body.velocity=(0,0)
	
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
	cylinder.body.apply_impulse_at_local_point((100,0))#set("imp", (100,0))
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
	cylinder.body.apply_impulse_at_local_point((100,0))#set("imp", (100,0))
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
	cylinder.body.apply_impulse_at_local_point((100,0))#set("imp", (100,0))
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

def staticCylinderSim(space, screen, options):
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
	cone.body.apply_impulse_at_local_point((100,53))#set("imp", (100,53))
	space.add(cone.body, cone.shape)
	
	cylinder = agents.agent(350, 400)
	cylinder.body = pymunk.Body(1,1, body_type=pymunk.Body.STATIC)
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

def mediumPushSim(space, screen, options):
	'''
	Simulation of Cylinder pushing Cone into Fireball over a medium distance
	before letting go.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 11: Medium Push Cylinder")
	# set up collision handlers
	ch0=space.add_collision_handler(0,2)
	ch0.data["surface"]=screen
	ch0.post_solve=rem0

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	
	cone = agents.patient(200, 300)
	space.add(cone.body, cone.shape)
	
	cylinder = agents.agent(150, 300)
	cylinder.body.apply_force_at_local_point((10000,0), (0,0))
	cylinder.shape.elasticity = 0
	space.add(cylinder.body, cylinder.shape)

	time = 70
	running = True
	while running:
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		time -= 1
		if time == 0:
			cylinder.body.velocity = (0,0)
		# set clock
		clock = pygame.time.Clock()
		# setup display and run sim
		screen.fill((255,255,255))
		space.step(1/50.0)
		space.debug_draw(options)
		pygame.display.flip()
		clock.tick(50)

	return

def longPushSim(space, screen, options):
	'''
	Simulation of Cylinder pushing Cone into Fireball over complete
	distance.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 12: Long Push Cylinder")
	# set up collision handlers
	ch0=space.add_collision_handler(0,2)
	ch0.data["surface"]=screen
	ch0.post_solve=rem0

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	
	cone = agents.patient(200, 300)
	space.add(cone.body, cone.shape)
	
	cylinder = agents.agent(150, 300)
	cylinder.body.apply_force_at_local_point((10000,0), (0,0))
	cylinder.shape.elasticity = 0
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

def touchSim(space, screen, options):
	'''
	Simulation of Cylinder touching Cone or tapping Cone into Fireball.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 13: Touch Cylinder")
	# set up collision handlers
	ch0=space.add_collision_handler(0,2)
	ch0.data["surface"]=screen
	ch0.post_solve=rem0

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	
	cone = agents.patient(200, 300)
	space.add(cone.body, cone.shape)
	
	cylinder = agents.agent(170, 300)
	cylinder.body.apply_impulse_at_local_point((200,0))
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

def doubleTouch(space, screen, options):
	'''
	Simulation of Cylinder tapping Cone twice into Fireball.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 10: Double Touch")
	# set up collision handlers
	ch0=space.add_collision_handler(0,2)
	ch0.data["surface"]=screen
	ch0.post_solve=rem0

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	
	cone = agents.patient(300, 300)
	space.add(cone.body, cone.shape)
	
	cylinder = agents.agent(170, 300)
	cylinder.body.apply_impulse_at_local_point((200,0))
	space.add(cylinder.body, cylinder.shape)

	time=80
	running = True
	while running:
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		time-=1
		if time == 30:
			cylinder.body.apply_impulse_at_local_point((600,0))
		elif time == 0:
			cylinder.body.velocity = (0,0)
		# set clock
		clock = pygame.time.Clock()
		# setup display and run sim
		screen.fill((255,255,255))
		space.step(1/50.0)
		space.debug_draw(options)
		pygame.display.flip()
		clock.tick(50)

	return

def dodgingSim(space, screen, options):
	pygame.display.set_caption("Simulation 9: Dodging Cylinder")
	# set up collision handlers
	ch0=space.add_collision_handler(0,2)
	ch0.data["surface"]=screen
	ch0.post_solve=rem0

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	
	cone = agents.patient(200, 300)
	cone.body.apply_impulse_at_local_point((130,0))
	space.add(cone.body, cone.shape)
	
	cylinder = agents.agent(400, 300)
	space.add(cylinder.body, cylinder.shape)

	time=80
	running = True
	while running:
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		time-=1
		if time == 30:
			cylinder.body.apply_impulse_at_local_point((0,100))
		elif time == 0:
			cylinder.body.velocity = (0,0)
		# set clock
		clock = pygame.time.Clock()
		# setup display and run sim
		screen.fill((255,255,255))
		space.step(1/50.0)
		space.debug_draw(options)
		pygame.display.flip()
		clock.tick(50)

	return

def fastCollisionSim(space, screen, options):
	pygame.display.set_caption("Simulation 9: Fast Collision Cylinder")
	# set up collision handlers
	ch0=space.add_collision_handler(0,2)
	ch0.data["surface"]=screen
	ch0.post_solve=rem0

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	

	cone = agents.patient(300, 300)
	cone.body.apply_impulse_at_local_point((30,0))
	space.add(cone.body, cone.shape)
	
	cylinder = agents.agent(100, 300)
	cylinder.body.apply_impulse_at_local_point((200,0))
	space.add(cylinder.body, cylinder.shape)

	time = 80
	running = True
	while running:
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		time-=1
		if time==0:
			cylinder.body.velocity=(0,0)
		clock = pygame.time.Clock()
		# setup display and run sim
		screen.fill((255,255,255))
		space.step(1/50.0)
		space.debug_draw(options)
		pygame.display.flip()
		clock.tick(50)

	return

def slowCollisionSim(space, screen, options):
	pygame.display.set_caption("Simulation 8: Slow Collision Cylinder")
	# set up collision handlers
	ch0=space.add_collision_handler(0,2)
	ch0.data["surface"]=screen
	ch0.post_solve=rem0
	ch1=space.add_collision_handler(0,1)
	ch1.data["surface"]=screen
	ch1.post_solve=rem1

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	
	
	cone = agents.patient(250, 300)
	cone.body.apply_impulse_at_local_point((100,0))
	space.add(cone.body, cone.shape)
	
	cylinder = agents.agent(100, 300)
	cylinder.body.apply_impulse_at_local_point((200,0))
	space.add(cylinder.body, cylinder.shape)

	time = 80
	running = True
	while running:
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		time-=1
		if time==0:
			cylinder.body.velocity=(0,0)
		clock = pygame.time.Clock()
		# setup display and run sim
		screen.fill((255,255,255))
		space.step(1/50.0)
		space.debug_draw(options)
		pygame.display.flip()
		clock.tick(50)

	return

def test(space, screen, options):
	pygame.display.set_caption("Simulation 2: Medium Distance")
	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"]=screen
	ch0.post_solve=rem0
	space.damping = 0.2

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	
	cone = agents.patient(400, 300)
	space.add(cone.body, cone.shape)
	
	cylinder = agents.agent(175, 300)
	cylinder.body.apply_impulse_at_local_point((100,0))#set("imp", (100,0))
	space.add(cylinder.body, cylinder.shape)

	total = [100]
	running = True
	while running:
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		print(cylinder.body.velocity)
		if (cylinder.body.velocity[0] < 100):
			imp = 100.0 - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((2*imp,0))
			total.append(imp)
		# set clock
		clock = pygame.time.Clock()
		# setup display and run sim
		screen.fill((255,255,255))
		space.step(1/50.0)
		space.debug_draw(options)
		pygame.display.flip()
		clock.tick(50)
		print("Total impulse: ", sum(total))
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

	test(space, screen, drawOptions)

if __name__ == '__main__':
	sys.exit(main())