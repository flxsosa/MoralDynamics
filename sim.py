'''
Simulations for Moral Dynamics

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

Key:
In Progress: May not be functional but working on it
Complete/Edit: Functions as needed but may need edits or optimizations
Complete: Functions and is optimal

March 10, 2017
Felix Sosa
'''

import pymunk
import pygame
import agents
import handlers
import math
import pymunk.pygame_util
from pygame.locals import *
import sys

# MODEL PARAMETERS

DYN_FRICTION = 0.2
STAT_FRICTION = 0.2
APMASS = 1
FMASS = 1

def shortDistance(space, screen, options, guess=False, impulse=200.0):
	'''
	Simulation of Cylinder pushing Cone into Fireball from a short distance
	away. Originally to be compared with longDistanceSim in Moral Kinematics.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 1: Short Distance")
	
	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2

	# dynamic friction
	space.damping = DYN_FRICTION
	
	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	cone = agents.patient(400, 300)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(250, 300)
	space.add(cylinder.body, cylinder.shape)
	
	# lists for impulses per timestep, total impulses, running flag, and ticks
	xImpsAgent = []
	yImpsAgent = []
	xImpsPatient = []
	yImpsPatient = []
	xImpsFireball = []
	yImpsFireball = []
	total = []
	running = True
	tick = 0

	# run simulation
	while running and tick<95:
		tick += 1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# static friction for all bodies
		if (cylinder.body.velocity == (0,0)):
			cylinder.body.update_velocity(cylinder.body, (0,0), STAT_FRICTION, 1/50.0)
		if (cone.body.velocity == (0,0)):
			cone.body.update_velocity(cone.body, (0,0), STAT_FRICTION, 1/50.0)
		if (ball.body.velocity == (0,0)):
			ball.body.update_velocity(ball.body, (0,0), STAT_FRICTION, 1/50.0)
		
		# keep the Agent at it's intended velocity for some duration
		if (cylinder.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((2*imp,0))
			total.append(2*imp)

		# append positional values to each list
		xImpsAgent.append(cylinder.body.position[0])
		yImpsAgent.append(cylinder.body.position[1])
		xImpsPatient.append(cone.body.position[0])
		yImpsPatient.append(cone.body.position[1])
		xImpsFireball.append(ball.body.position[0])
		yImpsFireball.append(ball.body.position[1])

		# set clock
		clock = pygame.time.Clock()
		
		# setup display and run sim based on whether it's truth or guess
		if(not guess):
			screen.fill((255,255,255))
		space.step(1/50.0)
		if(not guess):
			space.debug_draw(options)
			pygame.display.flip()
		if(not guess):
			clock.tick(50)
		else:
			clock.tick(500000)
		
		
	# remove value from collision list
	try:
		handlers.collision = []
	except:
		print("Exited before collision.")

	# output to user and return sum(total)#tuple
	print("Total impulse: ", sum(total))
	return sum(total)#(xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, xImpsFireball, yImpsFireball)

def mediumDistance(space, screen, options, guess=False, impulse=200):
	'''
	Simulation of Cylinder pushing Cone into Fireball from a medium distance
	away. Originally to be compared with shortDistanceSim in Moral Kinematics.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 2: Medium Distance")

	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"]=screen
	ch0.post_solve=handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"]=screen
	ch1.begin=handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	cone = agents.patient(400, 300)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(175, 300)
	space.add(cylinder.body, cylinder.shape)
	
	# lists for impulse values at each timestep, total impulses, runnign flag, and ticks
	xImpsAgent = []
	yImpsAgent = []
	xImpsPatient = []
	yImpsPatient = []
	xImpsFireball = []
	yImpsFireball = []
	total=[]
	running = True
	tick = 0

	# run simulation
	while running and tick<115:
		tick += 1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# static friction for all bodies
		if (cylinder.body.velocity == (0,0)):
			cylinder.body.update_velocity(cylinder.body, (0,0), STAT_FRICTION, 1/50.0)
		if (cone.body.velocity == (0,0)):
			cone.body.update_velocity(cone.body, (0,0), STAT_FRICTION, 1/50.0)
		if (ball.body.velocity == (0,0)):
			ball.body.update_velocity(ball.body, (0,0), STAT_FRICTION, 1/50.0)

		# keep the Agent at it's intended velocity for some duration
		if (cylinder.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((2*imp,0))
			total.append(2*imp)

		# append positional values to each list
		xImpsAgent.append(cylinder.body.position[0])
		yImpsAgent.append(cylinder.body.position[1])
		xImpsPatient.append(cone.body.position[0])
		yImpsPatient.append(cone.body.position[1])
		xImpsFireball.append(ball.body.position[0])
		yImpsFireball.append(ball.body.position[1])

		# set clock
		clock = pygame.time.Clock()

		# setup display and run sim based on whether it's truth or guess
		if(not guess):
			screen.fill((255,255,255))
		space.step(1/50.0)
		if(not guess):
			space.debug_draw(options)
			pygame.display.flip()
		if(not guess):
			clock.tick(50)
		else:
			clock.tick(500000)
		

	# remove value from collision list
	try:
		handlers.collision = []
	except:
		print "Exited before collision."

	# output to user and return sum(total)#tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return sum(total)#(xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, xImpsFireball, yImpsFireball)

def longDistance(space, screen, options, guess=False, impulse=200):
	'''
	Simulation of Cylinder pushing Cone into Fireball from a long distance
	away. Originally to be compared with shortDistanceSim in Moral Kinematics.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 3: Long Distance")

	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	cone = agents.patient(400, 300)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(100, 300)
	space.add(cylinder.body, cylinder.shape)
	
	# lists for impulse values at each timestep, total impulses, runnign flag, and ticks
	xImpsAgent = []
	yImpsAgent = []
	xImpsPatient = []
	yImpsPatient = []
	xImpsFireball = []
	yImpsFireball = []
	total = []
	running = True
	tick = 0

	# run simulation
	while running and tick < 133:
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# static friction for all bodies
		if (cylinder.body.velocity == (0,0)):
			cylinder.body.update_velocity(cylinder.body, (0,0), STAT_FRICTION, 1/50.0)
		if (cone.body.velocity == (0,0)):
			cone.body.update_velocity(cone.body, (0,0), STAT_FRICTION, 1/50.0)
		if (ball.body.velocity == (0,0)):
			ball.body.update_velocity(ball.body, (0,0), STAT_FRICTION, 1/50.0)

		# keep the Agent at it's intended velocity for some duration
		if (cylinder.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((2*imp,0))
			total.append(2*imp)

		# append positional values to each list
		xImpsAgent.append(cylinder.body.position[0])
		yImpsAgent.append(cylinder.body.position[1])
		xImpsPatient.append(cone.body.position[0])
		yImpsPatient.append(cone.body.position[1])
		xImpsFireball.append(ball.body.position[0])
		yImpsFireball.append(ball.body.position[1])

		# set clock
		clock = pygame.time.Clock()

		# setup display and run sim based on whether it's truth or guess
		if(not guess):
			screen.fill((255,255,255))
		space.step(1/50.0)
		if(not guess):
			space.debug_draw(options)
			pygame.display.flip()
		if(not guess):
			clock.tick(50)
		else:
			clock.tick(500000)
		

	# remove value from collision list and print out resulting effort
	try:
		handlers.collision = []
	except:
		print("Exited before collision.")

	# output to user and return sum(total)#tuple
	print("Total impulse: ", sum(total), "Tick ", tick)
	return sum(total)#(xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, xImpsFireball, yImpsFireball)

def static(space, screen, options, guess=False, impulse=350):
	'''
	Simulation of Cone bouncing off of a static Cylinder into a Fireball.
	Originally to be compared with shortDistance in Moral Kinematics.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space

	TODO: Consider ways to implement guessing of y-axis impulse on patient.
	'''
	if (not guess):
		pygame.display.set_caption("Simulation 4: Static Cylinder")

	# set up collision handlers
	ch0 = space.add_collision_handler(0,2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0,1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	ch1.post_solve = handlers.rem3
	space.damping = DYN_FRICTION

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	cone = agents.patient(200, 300)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(350, 400)
	space.add(cylinder.body, cylinder.shape)

	# lists for impulse values at each timestep, total impulses, runnign flag, and ticks
	xImpsAgent = []
	yImpsAgent = []
	xImpsPatient = []
	yImpsPatient = []
	xImpsFireball = []
	yImpsFireball = []
	total = []
	running = True
	tick = 0
	count = 0

	# run simulation
	while running and tick < 140:
		tick+=1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# static friction for all bodies
		if (cylinder.body.velocity == (0,0)):
			cylinder.body.update_velocity(cylinder.body, (0,0), STAT_FRICTION, 1/50.0)
		if (cone.body.velocity == (0,0)):
			cone.body.update_velocity(cone.body, (0,0), STAT_FRICTION, 1/50.0)
		if (ball.body.velocity == (0,0)):
			ball.body.update_velocity(ball.body, (0,0), STAT_FRICTION, 1/50.0)

		# keep the Patient at it's intended velocity for some duration
		if (cone.body.velocity[0] < impulse and cone.body.velocity[1] < 180 and \
				len(handlers.collision) == 0):
			impx = impulse - cone.body.velocity[0]
			impy = 180 - cone.body.velocity[1]
			cone.body.apply_impulse_at_local_point((impx,impy))

		# if collision between agent and patient, have agent push back once
		if (len(handlers.collision) != 0 and count==0):
			count+=1
			try:
				cylinder.body.apply_impulse_at_local_point((handlers.totalImpulse[0][0], 
					handlers.totalImpulse[0][1]))
				total.append(math.fabs(handlers.totalImpulse[0][0]) + \
					math.fabs(handlers.totalImpulse[0][1]))
			except:
				pass
		
		# append positional values to each list
		xImpsAgent.append(cylinder.body.position[0])
		yImpsAgent.append(cylinder.body.position[1])
		xImpsPatient.append(cone.body.position[0])
		yImpsPatient.append(cone.body.position[1])
		xImpsFireball.append(ball.body.position[0])
		yImpsFireball.append(ball.body.position[1])

		# set clock
		clock = pygame.time.Clock()

		# setup display and run sim based on whether it's truth or guess
		if(not guess):
			screen.fill((255,255,255))
		space.step(1/50.0)
		if(not guess):
			space.debug_draw(options)
			pygame.display.flip()
		if(not guess):
			clock.tick(50)
		else:
			clock.tick(500000)
		

	# remove value from collision list and print out resulting effort
	try:
		handlers.collision = []
		handlers.totalImpulse = []
	except:
		print("Exited before collision.")

	# output to user and return sum(total)#tuple
	print("Total impulse: ", sum(total), "Tick ", tick)
	return sum(total)#(xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, xImpsFireball, yImpsFireball)

def uphill(space, screen, options, guess=False, impulse=None):
	print("Uphill simulation not implemented yet.")
	return

def downhill(space, screen, options, guess=False, impulse=None):
	print("Downhill simulation not implemented yet.")
	return

def slowCollision(space, screen, options, guess=False, impulse=400):
	'''
	Simulation of Cone travelling slower after being hit by Cylinder.
	screen -- pygame display Surface
	options -- draw options for pymunk space
	TODO: 
	1. Clean up this simulation. Make it more clear the patient is 
	resiting the agent's push.
	2. Find a way to incorporate patients impulses into guess.
	'''
	if(not guess):
		pygame.display.set_caption("Simulation 7: Slow Collision Cylinder")

	# set up collision handlers
	ch0 = space.add_collision_handler(0,2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0,1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = 0.2

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	cone = agents.patient(200,300)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(100, 300)
	space.add(cylinder.body, cylinder.shape)
	
	# lists for impulse values at each timestep, total impulses, runnign flag, and ticks
	xImpsAgent = []
	yImpsAgent = []
	xImpsPatient = []
	yImpsPatient = []
	xImpsFireball = []
	yImpsFireball = []
	total=[]
	running = True
	tick = 0
	count = 0

	# run simulation
	while running and tick<149:
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# static friction for all bodies
		if (cylinder.body.velocity == (0,0)):
			cylinder.body.update_velocity(cylinder.body, (0,0), STAT_FRICTION, 1/50.0)
		if (cone.body.velocity == (0,0)):
			cone.body.update_velocity(cone.body, (0,0), STAT_FRICTION, 1/50.0)
		if (ball.body.velocity == (0,0)):
			ball.body.update_velocity(ball.body, (0,0), STAT_FRICTION, 1/50.0)

		# keep the Patient and Agent at their intended velocity for some duration
		if (cone.body.velocity[0] < 200 and len(handlers.collision) == 0):
			imp = 150 - cone.body.velocity[0]
			cone.body.apply_impulse_at_local_point((imp,0))
		if (cylinder.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = 450 - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)

		# when Agent and Patient collide, have Patient push back and Agent stop
		if (len(handlers.collision) == 1 and count == 0):
			count+=1
			cone.body.apply_impulse_at_local_point((-50,0))
			cylinder.body.apply_impulse_at_local_point((-1*cylinder.body.velocity[0],0))
			total.append(math.fabs(cylinder.body.velocity[0]))

		# append positional values to each list
		xImpsAgent.append(cylinder.body.position[0])
		yImpsAgent.append(cylinder.body.position[1])
		xImpsPatient.append(cone.body.position[0])
		yImpsPatient.append(cone.body.position[1])
		xImpsFireball.append(ball.body.position[0])
		yImpsFireball.append(ball.body.position[1])

		# set clock
		clock = pygame.time.Clock()

		# setup display and run sim based on whether it's truth or guess
		if(not guess):
			screen.fill((255,255,255))
		space.step(1/50.0)
		if(not guess):
			space.debug_draw(options)
			pygame.display.flip()
		if(not guess):
			clock.tick(50)
		else:
			clock.tick(500000)
		
	# remove value from collision list and print out resulting effort
	try:
		handlers.collision = []
		handlers.totalImpulse = []
	except:
		print "Exited before collision."

	# output to user and return sum(total)#tuple
	print "Total impulse: ", sum(total), "Tick: ", tick
	return sum(total)#(xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, xImpsFireball, yImpsFireball)

def fastCollision(space, screen, options, guess=False, impulse=400):
	'''
	Simulation of Cone travelling faster after being hit by Cylinder.
	screen -- pygame display Surface
	options -- draw options for pymunk space
	TODO:
	1. Clean up this simulation. Make it more clear the patient is 
	going faster after the agent's push.
	2. Find a way to incorporate patient's impulses into guess.
	'''
	if(not guess):
		pygame.display.set_caption("Simulation 8: Fast Collision Cylinder")

	# set up collision handlers
	ch0 = space.add_collision_handler(0,2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0,1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = 0.2
	
	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	cone = agents.patient(300, 300)
	space.add(cone.body, cone.shape)	
	cylinder = agents.agent(100, 300)
	space.add(cylinder.body, cylinder.shape)

	# lists for impulse values at each timestep, total impulses, runnign flag, and ticks
	xImpsAgent = []
	yImpsAgent = []
	xImpsPatient = []
	yImpsPatient = []
	xImpsFireball = []
	yImpsFireball = []
	total=[]
	running = True
	tick = 0

	# run simulation
	while running and tick<154:
		tick+=1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# static friction for all bodies
		if (cylinder.body.velocity == (0,0)):
			cylinder.body.update_velocity(cylinder.body, (0,0), STAT_FRICTION, 1/50.0)
		if (cone.body.velocity == (0,0)):
			cone.body.update_velocity(cone.body, (0,0), STAT_FRICTION, 1/50.0)
		if (ball.body.velocity == (0,0)):
			ball.body.update_velocity(ball.body, (0,0), STAT_FRICTION, 1/50.0)

		# keep Agent and Patient at their intended velocities
		if (cone.body.velocity[0] < 30):
			imp = 30.0 - cone.body.velocity[0]
			cone.body.apply_impulse_at_local_point((imp,0))
		if (cylinder.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)

		# append positional values to each list
		xImpsAgent.append(cylinder.body.position[0])
		yImpsAgent.append(cylinder.body.position[1])
		xImpsPatient.append(cone.body.position[0])
		yImpsPatient.append(cone.body.position[1])
		xImpsFireball.append(ball.body.position[0])
		yImpsFireball.append(ball.body.position[1])

		# set clock
		clock = pygame.time.Clock()

		# setup display and run sim based on whether it's truth or guess
		if(not guess):
			screen.fill((255,255,255))
		space.step(1/50.0)
		if(not guess):
			space.debug_draw(options)
			pygame.display.flip()
		if(not guess):
			clock.tick(50)
		else:
			clock.tick(500000)
		
	# remove value from collision list and print out resulting effort
	try:
		handlers.collision = []
	except:
		print "Exited before collision."

	# output to user and return sum(total)#tuple
	print "Total impulse: ", sum(total), "Tick: ", tick
	return sum(total)#(xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, xImpsFireball, yImpsFireball)

def dodge(space, screen, options, guess=False, impulse=150):
	'''
	Simulation of Cylinder dodging Cone as it runs into Fireball.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	TODO:
	1. See if there's a better way to deal with the time variable
	'''
	if(not guess):
		pygame.display.set_caption("Simulation 9: Dodging Cylinder")
	# set up collision handlers
	ch0 = space.add_collision_handler(0,2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	space.damping = 0.2

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	cone = agents.patient(200, 300)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(400, 300)
	space.add(cylinder.body, cylinder.shape)

	# lists for impulse values at each timestep, total impulses, runnign flag, and ticks
	xImpsAgent = []
	yImpsAgent = []
	xImpsPatient = []
	yImpsPatient = []
	xImpsFireball = []
	yImpsFireball = []
	total = []
	running = True
	tick = 0
	time = 80

	# run simulation
	while running and tick<186:
		tick+=1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# static friction for all bodies
		if (cylinder.body.velocity == (0,0)):
			cylinder.body.update_velocity(cylinder.body, (0,0), STAT_FRICTION, 1/50.0)
		if (cone.body.velocity == (0,0)):
			cone.body.update_velocity(cone.body, (0,0), STAT_FRICTION, 1/50.0)
		if (ball.body.velocity == (0,0)):
			ball.body.update_velocity(ball.body, (0,0), STAT_FRICTION, 1/50.0)

		# keep Patient at it's intended velocity
		if (cone.body.velocity[0] < 100):
			imp = 100 - cone.body.velocity[0]
			cone.body.apply_impulse_at_local_point((imp,0))

		# at t == 20, Agent dogdes Patient
		time-=1
		if (time == 20):
			cylinder.body.apply_impulse_at_local_point((0,impulse))
			total.append(impulse)
		
		# append positional values to each list
		xImpsAgent.append(cylinder.body.position[0])
		yImpsAgent.append(cylinder.body.position[1])
		xImpsPatient.append(cone.body.position[0])
		yImpsPatient.append(cone.body.position[1])
		xImpsFireball.append(ball.body.position[0])
		yImpsFireball.append(ball.body.position[1])

		# set clock
		clock = pygame.time.Clock()

		# setup display and run sim based on whether it's truth or guess
		if(not guess):
			screen.fill((255,255,255))
		space.step(1/50.0)
		if(not guess):
			space.debug_draw(options)
			pygame.display.flip()
		if(not guess):
			clock.tick(50)
		else:
			clock.tick(500000)
		
	# output to user and return sum(total)#tuple
	print "Total impulse: ", sum(total), "Tick: ", tick
	return sum(total)#(xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, xImpsFireball, yImpsFireball)

def doubleTouch(space, screen, options, guess=False, impulse=170):
	'''
	Simulation of Cylinder tapping Cone twice into Fireball.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	if(not guess):
		pygame.display.set_caption("Simulation 10: Double Touch")

	# set up collision handlers
	ch0 = space.add_collision_handler(0,2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	cone = agents.patient(300, 300)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(170, 300)
	space.add(cylinder.body, cylinder.shape)

	# lists for impulse values at each timestep, total impulses, runnign flag, and ticks
	xImpsAgent = []
	yImpsAgent = []
	xImpsPatient = []
	yImpsPatient = []
	xImpsFireball = []
	yImpsFireball = []
	total = []
	running = True
	tick = 0
	time = 50

	# run simulation
	while running and tick<137:
		tick+=1
		time -= 1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# static friction for all bodies
		if (cylinder.body.velocity == (0,0)):
			cylinder.body.update_velocity(cylinder.body, (0,0), STAT_FRICTION, 1/50.0)
		if (cone.body.velocity == (0,0)):
			cone.body.update_velocity(cone.body, (0,0), STAT_FRICTION, 1/50.0)
		if (ball.body.velocity == (0,0)):
			ball.body.update_velocity(ball.body, (0,0), STAT_FRICTION, 1/50.0)

		# keep Agent at intended velocity
		if (cylinder.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((2*imp,0))
			total.append(2*imp)
		# when t == 10, the Agent collides with the Patient again
		elif (time == 10):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((2*imp,0))
			total.append(2*imp)
		elif (len(handlers.collision) == 2 and cylinder.body.velocity[0] != 0):
			cylinder.body.apply_impulse_at_local_point((-1*cylinder.body.velocity[0],0))
			total.append(math.fabs(imp))

		# append positional values to each list
		xImpsAgent.append(cylinder.body.position[0])
		yImpsAgent.append(cylinder.body.position[1])
		xImpsPatient.append(cone.body.position[0])
		yImpsPatient.append(cone.body.position[1])
		xImpsFireball.append(ball.body.position[0])
		yImpsFireball.append(ball.body.position[1])

		# set clock
		clock = pygame.time.Clock()

		# setup display and run sim based on whether it's truth or guess
		if(not guess):
			screen.fill((255,255,255))
		space.step(1/50.0)
		if(not guess):
			space.debug_draw(options)
			pygame.display.flip()
		if(not guess):
			clock.tick(50)
		else:
			clock.tick(500000)
		

	# remove value from collision list and print out resulting effort
	try:
		handlers.collision = []
	except:
		print "Exited before collision."

	# output to user and return sum(total)#tuple
	print "Total impulse: ", sum(total), "Tick: ", tick
	return sum(total)#(xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, xImpsFireball, yImpsFireball)

def mediumPush(space, screen, options, guess=False, impulse=150):
	'''
	Simulation of Cylinder pushing Cone into Fireball over a medium distance
	before letting go.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	TODO:
	1. Make pushing not time dependent but distance dependent
	'''
	if(not guess):
		pygame.display.set_caption("Simulation 11: Medium Push Cylinder")
	# set up collision handlers
	ch0 = space.add_collision_handler(0,2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	space.damping = DYN_FRICTION

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	cone = agents.patient(200, 300)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(150, 300)
	space.add(cylinder.body, cylinder.shape)

	# lists for impulse values at each timestep, total impulses, runnign flag, and ticks
	xImpsAgent = []
	yImpsAgent = []
	xImpsPatient = []
	yImpsPatient = []
	xImpsFireball = []
	yImpsFireball = []
	total = []
	running = True
	tick = 0
	time = 70

	# run simulation
	while running and tick<144:
		time -= 1
		tick += 1
		
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# static friction for all bodies
		if (cylinder.body.velocity == (0,0)):
			cylinder.body.update_velocity(cylinder.body, (0,0), STAT_FRICTION, 1/50.0)
		if (cone.body.velocity == (0,0)):
			cone.body.update_velocity(cone.body, (0,0), STAT_FRICTION, 1/50.0)
		if (ball.body.velocity == (0,0)):
			ball.body.update_velocity(ball.body, (0,0), STAT_FRICTION, 1/50.0)

		# keep Agent at intended velocity
		if (cylinder.body.velocity[0] < impulse and time > 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((2*imp,0))
			total.append(math.fabs(2*imp))

		# when t == 0, have Agent stop 
		if (time == 0):
			cylinder.body.apply_impulse_at_local_point((-1*cylinder.body.velocity[0],0))
		
		# append positional values to each list
		xImpsAgent.append(cylinder.body.position[0])
		yImpsAgent.append(cylinder.body.position[1])
		xImpsPatient.append(cone.body.position[0])
		yImpsPatient.append(cone.body.position[1])
		xImpsFireball.append(ball.body.position[0])
		yImpsFireball.append(ball.body.position[1])

		# set clock
		clock = pygame.time.Clock()

		# setup display and run sim based on whether it's truth or guess
		if(not guess):
			screen.fill((255,255,255))
		space.step(1/50.0)
		if(not guess):
			space.debug_draw(options)
			pygame.display.flip()
		if(not guess):
			clock.tick(50)
		else:
			clock.tick(500000)
		
	# handlers.remove value from collision list and print out resulting effort
	try:
		handlers.collision = []
	except:
		print "Exited before collision."

	# output to user and return sum(total)#tuple
	print "Total impulse: ", sum(total), "Tick: ", tick
	return sum(total)#(xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, xImpsFireball, yImpsFireball)

def longPush(space, screen, options, guess=False, impulse=100):
	'''
	Simulation of Cylinder pushing Cone into Fireball over complete
	distance.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	if(not guess):
		pygame.display.set_caption("Simulation 12: Long Push Cylinder")
	# set up collision handlers
	ch0 = space.add_collision_handler(0,2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch0.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)	
	cone = agents.patient(200, 300)
	space.add(cone.body, cone.shape)	
	cylinder = agents.agent(150, 300)
	space.add(cylinder.body, cylinder.shape)

	# lists for impulse values at each timestep, total impulses, runnign flag, and ticks
	xImpsAgent = []
	yImpsAgent = []
	xImpsPatient = []
	yImpsPatient = []
	xImpsFireball = []
	yImpsFireball = []
	total=[]
	running = True
	tick = 0

	# run simulation
	while running and tick<183:
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# static friction for all bodies
		if (cylinder.body.velocity == (0,0)):
			cylinder.body.update_velocity(cylinder.body, (0,0), STAT_FRICTION, 1/50.0)
		if (cone.body.velocity == (0,0)):
			cone.body.update_velocity(cone.body, (0,0), STAT_FRICTION, 1/50.0)
		if (ball.body.velocity == (0,0)):
			ball.body.update_velocity(ball.body, (0,0), STAT_FRICTION, 1/50.0)

		# keep Agent at intended velocity
		if (cylinder.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((2*imp,0))
			total.append(2*imp)

		# append positional values to each list
		xImpsAgent.append(cylinder.body.position[0])
		yImpsAgent.append(cylinder.body.position[1])
		xImpsPatient.append(cone.body.position[0])
		yImpsPatient.append(cone.body.position[1])
		xImpsFireball.append(ball.body.position[0])
		yImpsFireball.append(ball.body.position[1])

		# set clock
		clock = pygame.time.Clock()

		# setup display and run sim based on whether it's truth or guess
		if(not guess):
			screen.fill((255,255,255))
		space.step(1/50.0)
		if(not guess):
			space.debug_draw(options)
			pygame.display.flip()
		if(not guess):
			clock.tick(50)
		else:
			clock.tick(500000)
		
	# remove value from collision list and print out resulting effort
	try:
		handlers.collision = []
	except:
		print "Exited before collision."
	print "Total impulse: ", sum(total), "Tick: ", tick
	return sum(total)#(xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, xImpsFireball, yImpsFireball)

def touch(space, screen, options, guess=False, impulse=250):
	'''
	Simulation of Cylinder touching Cone or tapping Cone into Fireball.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	if(not guess):
		pygame.display.set_caption("Simulation 13: Touch Cylinder")
	# set up collision handlers
	ch0 = space.add_collision_handler(0,2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	cone = agents.patient(200, 300)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(170, 300)
	space.add(cylinder.body, cylinder.shape)

	# lists for impulse values at each timestep, total impulses, runnign flag, and ticks
	xImpsAgent = []
	yImpsAgent = []
	xImpsPatient = []
	yImpsPatient = []
	xImpsFireball = []
	yImpsFireball = []
	total = []
	running = True
	tick = 0

	# run simulation
	while running and tick<114:
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# static friction for all bodies
		if (cylinder.body.velocity == (0,0)):
			cylinder.body.update_velocity(cylinder.body, (0,0), STAT_FRICTION, 1/50.0)
		if (cone.body.velocity == (0,0)):
			cone.body.update_velocity(cone.body, (0,0), STAT_FRICTION, 1/50.0)
		if (ball.body.velocity == (0,0)):
			ball.body.update_velocity(ball.body, (0,0), STAT_FRICTION, 1/50.0)
		
		# keep Agent at intended velocity
		if (cylinder.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((2*imp,0))
			total.append(2*imp)

		# append positional values to each list
		xImpsAgent.append(cylinder.body.position[0])
		yImpsAgent.append(cylinder.body.position[1])
		xImpsPatient.append(cone.body.position[0])
		yImpsPatient.append(cone.body.position[1])
		xImpsFireball.append(ball.body.position[0])
		yImpsFireball.append(ball.body.position[1])

		# set clock
		clock = pygame.time.Clock()

		# setup display and run sim based on whether it's truth or guess
		if(not guess):
			screen.fill((255,255,255))
		space.step(1/50.0)
		if(not guess):
			space.debug_draw(options)
			screen.blit(logo_img, p)
			pygame.display.flip()
		if(not guess):
			clock.tick(50)
		else:
			clock.tick(500000)
		

	# remove value from collision list and print out resulting effort
	try:
		handlers.collision = []
	except:
		print "Exited before collision."

	print "Total impulse: ", sum(total), "Tick: ", tick
	return sum(total)#(xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, xImpsFireball, yImpsFireball)

def pushFireball(space, screen, options, guess=False, impulse=275):
	'''
	Simulation of Cylinder pushing Fireball into Cone.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	if(not guess):
		pygame.display.set_caption("Simulation 14: Push Fireball")
	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(1, 2)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	ball = agents.fireball(400, 300)
	space.add(ball.body, ball.shape)
	cone = agents.patient(500, 300)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(100, 300)
	space.add(cylinder.body, cylinder.shape)
	
	# lists for impulse values at each timestep, total impulses, runnign flag, and ticks
	xImpsAgent = []
	yImpsAgent = []
	xImpsPatient = []
	yImpsPatient = []
	xImpsFireball = []
	yImpsFireball = []
	total = []
	running = True
	tick = 0

	# run simulation
	while running and tick<143:
		tick+=1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# static friction for all bodies
		if (cylinder.body.velocity == (0,0)):
			cylinder.body.update_velocity(cylinder.body, (0,0), STAT_FRICTION, 1/50.0)
		if (cone.body.velocity == (0,0)):
			cone.body.update_velocity(cone.body, (0,0), STAT_FRICTION, 1/50.0)
		if (ball.body.velocity == (0,0)):
			ball.body.update_velocity(ball.body, (0,0), STAT_FRICTION, 1/50.0)

		# keep Agent at intended velocity until Fireball hits Patient
		if (cylinder.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((2*imp,0))
			total.append(2*imp)
		elif (len(handlers.collision) != 0 and cylinder.body.velocity[0] != 0):
			cylinder.body.apply_impulse_at_local_point((-1*cylinder.body.velocity[0],0))
			total.append(math.fabs(imp))

		# append positional values to each list
		xImpsAgent.append(cylinder.body.position[0])
		yImpsAgent.append(cylinder.body.position[1])
		xImpsPatient.append(cone.body.position[0])
		yImpsPatient.append(cone.body.position[1])
		xImpsFireball.append(ball.body.position[0])
		yImpsFireball.append(ball.body.position[1])

		# set clock
		clock = pygame.time.Clock()

		# setup display and run sim based on whether it's truth or guess
		if(not guess):
			screen.fill((255,255,255))
		space.step(1/50.0)
		if(not guess):
			space.debug_draw(options)
			pygame.display.flip()
		if(not guess):
			clock.tick(50)
		else:
			clock.tick(500000)
		

	# remove value from collision list and print out resulting effort
	try:
		handlers.collision = []
	except:
		print "Exited before collision."

	# output to user and return sum(total)#tuple
	print "Total impulse: ", sum(total), "Tick: ", tick
	return sum(total)#(xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, xImpsFireball, yImpsFireball)