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
import glob

# MODEL PARAMETERS

DYN_FRICTION = 0.6
STAT_FRICTION = 0.1
AP_MASS = 1
F_MASS = 1
AGENT_RUNNING = 300
AGENT_WALKING = 150

# SPRITES
BACKGROUND_S = pygame.image.load("Sprites/sand.jpg")
BACKGROUND_G = pygame.image.load("Sprites/grass.jpg")
fireSprite = pygame.image.load("Sprites/FIRE.png")
patientSprite = pygame.image.load("Sprites/Patient.png")
agentSprite = pygame.image.load("Sprites/Agent.png")

# PATIENT-AGENT ANIMATION SPRITES
ani = glob.glob("Sprites/fireball*.png")
ani.sort()

def setBackground(screen):
	'''
	Sets the background for simulations. Expected screen
	of (1000px,600px).
	'''
	# top grass row
	screen.blit(BACKGROUND_G, (0,0))
	screen.blit(BACKGROUND_G, (200,0))
	screen.blit(BACKGROUND_G, (400,0))
	screen.blit(BACKGROUND_G, (600,0))
	screen.blit(BACKGROUND_G, (800,0))
	# bottom grass row
	screen.blit(BACKGROUND_G, (0,400))
	screen.blit(BACKGROUND_G, (200,400))
	screen.blit(BACKGROUND_G, (400,400))
	screen.blit(BACKGROUND_G, (600,400))
	screen.blit(BACKGROUND_G, (800,400))
	# sand row
	screen.blit(BACKGROUND_S, (0,200))
	screen.blit(BACKGROUND_S, (200,200))
	screen.blit(BACKGROUND_S, (400,200))
	screen.blit(BACKGROUND_S, (600,200))
	screen.blit(BACKGROUND_S, (800,200))

def shortDistance(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	ball = agents.fireball(900, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(800, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(500, 300, AP_MASS)
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

	# animation flag and counter
	x = 0
	cnt = 0

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-60)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		tick += 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# static friction for all bodies
		if (cylinder.body.velocity[0] == (0,0)):
			cylinder.body.update_velocity(cylinder.body, (0,0), STAT_FRICTION, 1/50.0)
		if (cone.body.velocity == (0,0)):
			cone.body.update_velocity(cone.body, (0,0), STAT_FRICTION, 1/50.0)
		if (ball.body.velocity == (0,0)):
			ball.body.update_velocity(ball.body, (0,0), STAT_FRICTION, 1/50.0)
		
		# keep the Agent at it's intended velocity for some duration
		if (cylinder.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		elif (len(handlers.collision) == 1):
			imp = cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((-1*imp,0))
			total.append(math.fabs(imp))

		# append positional values to each list
		xImpsAgent.append(cylinder.body.position[0])
		yImpsAgent.append(cylinder.body.position[1])
		xImpsPatient.append(cone.body.position[0])
		yImpsPatient.append(cone.body.position[1])
		xImpsFireball.append(ball.body.position[0])
		yImpsFireball.append(ball.body.position[1])

		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			setBackground(screen)
			screen.blit(fireSprite, pBall)
			screen.blit(patientSprite, pCone)
			screen.blit(agentSprite, pAgent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)

	# patient collision
	for i in range(25):
		screen.fill((255,255,255))
		space.debug_draw(options)
		setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		if (cnt < 12 and x == 0):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt += 1
			if cnt == 12:
				x = 1
				cnt = 11
		elif (cnt >= 0 and x == 1):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt -= 1
		else:
			screen.blit(fireSprite, pBall)
			screen.blit(agentSprite, pAgent)

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# output to user and return tuple
	print "Total impulse: ", sum(total)
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def mediumDistance(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	ball = agents.fireball(900, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(800, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(300, 300, AP_MASS)
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

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-60)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
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
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		if (len(handlers.collision) == 1):
			imp = cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((-1*imp,0))
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
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			setBackground(screen)
			screen.blit(fireSprite, pBall)
			screen.blit(patientSprite, pCone)
			screen.blit(agentSprite, pAgent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)	

	# patient collision
	for i in range(25):
		screen.fill((255,255,255))
		space.debug_draw(options)
		setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		if (cnt < 12 and x == 0):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt += 1
			if cnt == 12:
				x = 1
				cnt = 11
		elif (cnt >= 0 and x == 1):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt -= 1
		else:
			screen.blit(fireSprite, pBall)
			screen.blit(agentSprite, pAgent)

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def longDistance(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	ball = agents.fireball(900, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(800, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(100, 300, AP_MASS)
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

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-60)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
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
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		if (len(handlers.collision) == 1):
			imp = cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((-1*imp,0))
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
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			setBackground(screen)
			screen.blit(fireSprite, pBall)
			screen.blit(patientSprite, pCone)
			screen.blit(agentSprite, pAgent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)	

	# patient collision
	for i in range(25):
		screen.fill((255,255,255))
		space.debug_draw(options)
		setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		if (cnt < 12 and x == 0):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt += 1
			if cnt == 12:
				x = 1
				cnt = 11
		elif (cnt >= 0 and x == 1):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt -= 1
		else:
			screen.blit(fireSprite, pBall)
			screen.blit(agentSprite, pAgent)

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def static(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Simulation of Cone bouncing off of a static Cylinder into a Fireball.
	Originally to be compared with shortDistance in Moral Kinematics.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
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
	ball = agents.fireball(800, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(300, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(600, 500, AP_MASS)
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

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-60)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
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
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			setBackground(screen)
			screen.blit(fireSprite, pBall)
			screen.blit(patientSprite, pCone)
			screen.blit(agentSprite, pAgent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)	

	# patient collision
	for i in range(25):
		screen.fill((255,255,255))
		space.debug_draw(options)
		setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		if (cnt < 12 and x == 0):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt += 1
			if cnt == 12:
				x = 1
				cnt = 11
		elif (cnt >= 0 and x == 1):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt -= 1
		else:
			screen.blit(fireSprite, pBall)
			screen.blit(agentSprite, pAgent)

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
		handlers.totalImpulse = []
	except:
		print("Exited before collision.")

	# output to user and return tuple
	print("Total impulse: ", sum(total), "Tick ", tick)
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def uphill(space, screen, options, guess=False, impulse=None):
	print("Uphill simulation not implemented yet.")
	return

def downhill(space, screen, options, guess=False, impulse=None):
	print("Downhill simulation not implemented yet.")
	return

def slowCollision(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Simulation of Cone travelling slower after being hit by Cylinder.
	screen -- pygame display Surface
	options -- draw options for pymunk space
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
	space.damping = DYN_FRICTION

	# add shapes
	ball = agents.fireball(900, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(600,300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(400, 300, AP_MASS)
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

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-60)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Patient and Agent at their intended velocity for some duration
		if (cone.body.velocity[0] < AGENT_WALKING and len(handlers.collision) == 0):
			imp = AGENT_WALKING - cone.body.velocity[0]
			cone.body.apply_impulse_at_local_point((imp,0))
		if (cylinder.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)

		# when Agent and Patient collide, have Patient push back and Agent stop
		if (len(handlers.collision) == 1 and count == 0):
			count+=1
			cone.body.apply_impulse_at_local_point((-AGENT_WALKING,0))
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
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			setBackground(screen)
			screen.blit(fireSprite, pBall)
			screen.blit(patientSprite, pCone)
			screen.blit(agentSprite, pAgent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)	
		
	# patient collision
	for i in range(25):
		screen.fill((255,255,255))
		space.debug_draw(options)
		setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		if (cnt < 12 and x == 0):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt += 1
			if cnt == 12:
				x = 1
				cnt = 11
		elif (cnt >= 0 and x == 1):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt -= 1
		else:
			screen.blit(fireSprite, pBall)
			screen.blit(agentSprite, pAgent)

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick: ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def fastCollision(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Simulation of Cone travelling faster after being hit by Cylinder.
	screen -- pygame display Surface
	options -- draw options for pymunk space
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
	space.damping = DYN_FRICTION
	
	# add shapes
	ball = agents.fireball(900, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(600, 300, AP_MASS)
	space.add(cone.body, cone.shape)	
	cylinder = agents.agent(400, 300, AP_MASS)
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

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-60)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		tick+=1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep Agent and Patient at their intended velocities
		if (cone.body.velocity[0] < AGENT_WALKING and len(handlers.collision) == 0):
			imp = AGENT_WALKING - cone.body.velocity[0]
			cone.body.apply_impulse_at_local_point((imp,0))
		if (cylinder.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		
		# when Agent and Patient collide, have Patient push back and Agent stop
		if (len(handlers.collision) == 1):
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
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			setBackground(screen)
			screen.blit(fireSprite, pBall)
			screen.blit(patientSprite, pCone)
			screen.blit(agentSprite, pAgent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)	
		
	# patient collision
	for i in range(25):
		screen.fill((255,255,255))
		space.debug_draw(options)
		setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		if (cnt < 12 and x == 0):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt += 1
			if cnt == 12:
				x = 1
				cnt = 11
		elif (cnt >= 0 and x == 1):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt -= 1
		else:
			screen.blit(fireSprite, pBall)
			screen.blit(agentSprite, pAgent)

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick: ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def dodge(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	ch0.begin = handlers.rem2
	ch0.post_solve = handlers.rem0
	space.damping = DYN_FRICTION

	# add shapes
	ball = agents.fireball(900, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(400, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(800, 300, AP_MASS)
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

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-60)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		tick+=1
		time-=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep Patient at it's intended velocity
		if (cone.body.velocity[0] < AGENT_RUNNING):
			imp = AGENT_RUNNING - cone.body.velocity[0]
			cone.body.apply_impulse_at_local_point((imp,0))

		# at t == 20, Agent dogdes Patient
		if (time == 40):
			cylinder.body.apply_impulse_at_local_point((0,impulse))
			total.append(impulse)
		if (time == 25):
			imp = cylinder.body.velocity[1]
			cylinder.body.apply_impulse_at_local_point((0,-1*imp))
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
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			setBackground(screen)
			screen.blit(fireSprite, pBall)
			screen.blit(patientSprite, pCone)
			screen.blit(agentSprite, pAgent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)	
		
	# patient collision
	for i in range(25):
		screen.fill((255,255,255))
		space.debug_draw(options)
		setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		if (cnt < 12 and x == 0):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt += 1
			if cnt == 12:
				x = 1
				cnt = 11
		elif (cnt >= 0 and x == 1):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt -= 1
		else:
			screen.blit(fireSprite, pBall)
			screen.blit(agentSprite, pAgent)

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick: ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def doubleTouch(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	ball = agents.fireball(900, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(200, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(150, 300, AP_MASS)
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

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-60)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
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
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		# when t == 10, the Agent collides with the Patient again
		elif (time == 25):
			imp = impulse+200 - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
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
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			setBackground(screen)
			screen.blit(fireSprite, pBall)
			screen.blit(patientSprite, pCone)
			screen.blit(agentSprite, pAgent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)	
		
	# patient collision
	for i in range(25):
		screen.fill((255,255,255))
		space.debug_draw(options)
		setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		if (cnt < 12 and x == 0):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt += 1
			if cnt == 12:
				x = 1
				cnt = 11
		elif (cnt >= 0 and x == 1):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt -= 1
		else:
			screen.blit(fireSprite, pBall)
			screen.blit(agentSprite, pAgent)

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick: ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def mediumPush(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	ch0.begin = handlers.rem2
	ch0.post_solve = handlers.rem0
	space.damping = DYN_FRICTION

	# add shapes
	ball = agents.fireball(900, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(200, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(150, 300, AP_MASS)
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

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-60)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		time -= 1
		tick += 1
		
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep Agent at intended velocity
		if (time > 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(math.fabs(imp))

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
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			setBackground(screen)
			screen.blit(fireSprite, pBall)
			screen.blit(patientSprite, pCone)
			screen.blit(agentSprite, pAgent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)	
		
	# patient collision
	for i in range(25):
		screen.fill((255,255,255))
		space.debug_draw(options)
		setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		if (cnt < 12 and x == 0):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt += 1
			if cnt == 12:
				x = 1
				cnt = 11
		elif (cnt >= 0 and x == 1):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt -= 1
		else:
			screen.blit(fireSprite, pBall)
			screen.blit(agentSprite, pAgent)

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick: ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def longPush(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	ball = agents.fireball(900, 300, F_MASS)
	space.add(ball.body, ball.shape)	
	cone = agents.patient(200, 300, AP_MASS)
	space.add(cone.body, cone.shape)	
	cylinder = agents.agent(150, 300, AP_MASS)
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
	time = 100

	# animation flag and counter 
	x = 0
	cnt = 0

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-60)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		time -= 1
		tick += 1
		
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep Agent at intended velocity
		if (time > 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(math.fabs(imp))

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
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			setBackground(screen)
			screen.blit(fireSprite, pBall)
			screen.blit(patientSprite, pCone)
			screen.blit(agentSprite, pAgent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)	
		
	# patient collision
	for i in range(25):
		screen.fill((255,255,255))
		space.debug_draw(options)
		setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		if (cnt < 12 and x == 0):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt += 1
			if cnt == 12:
				x = 1
				cnt = 11
		elif (cnt >= 0 and x == 1):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt -= 1
		else:
			screen.blit(fireSprite, pBall)
			screen.blit(agentSprite, pAgent)

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."
	print "Total impulse: ", sum(total), "Tick: ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def touch(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	ball = agents.fireball(900, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(700, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(650, 300, AP_MASS)
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

	# animation flag and counter
	cnt = 0
	x = 0

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-60)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep Agent at intended velocity
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
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			setBackground(screen)
			screen.blit(fireSprite, pBall)
			screen.blit(patientSprite, pCone)
			screen.blit(agentSprite, pAgent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)	
		
	# patient collision
	for i in range(25):
		screen.fill((255,255,255))
		space.debug_draw(options)
		setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		if (cnt < 12 and x == 0):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt += 1
			if cnt == 12:
				x = 1
				cnt = 11
		elif (cnt >= 0 and x == 1):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt -= 1
		else:
			screen.blit(fireSprite, pBall)
			screen.blit(agentSprite, pAgent)

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	print "Total impulse: ", sum(total), "Tick: ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def pushFireball(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	ball = agents.fireball(200, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(900, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(100, 300, AP_MASS)
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
	time = 100

	# animation flag and counter 
	x = 0
	cnt = 0

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-60)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		time -= 1
		tick += 1
		
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep Agent at intended velocity
		if (time > 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(math.fabs(imp))

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
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			setBackground(screen)
			screen.blit(fireSprite, pBall)
			screen.blit(patientSprite, pCone)
			screen.blit(agentSprite, pAgent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)	
		
	# patient collision
	for i in range(25):
		screen.fill((255,255,255))
		space.debug_draw(options)
		setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		if (cnt < 12 and x == 0):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt += 1
			if cnt == 12:
				x = 1
				cnt = 11
		elif (cnt >= 0 and x == 1):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt -= 1
		else:
			screen.blit(fireSprite, pBall)
			screen.blit(agentSprite, pAgent)

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick: ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def test(space, screen, options, guess=False, impulse=100):
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

	DYN_FRICTION = 0.5
	STAT_FRICTION = None
	# dynamic friction
	space.damping = DYN_FRICTION
	
	# add shapes
	ball = agents.fireball(500, 300, F_MASS)
	#space.add(ball.body, ball.shape)
	cone = agents.patient(450, 300, AP_MASS)
	#space.add(cone.body, cone.shape)
	cylinder = agents.agent(300, 300, AP_MASS)
	space.add(cylinder.body, cylinder.shape)
	
	# load fireball sprite into simulation
	fireSprite = pygame.image.load("Plots/fireball.png")
	
	# lists for impulses per timestep, total impulses, running flag, and ticks
	total = []
	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0
	dist = []
	cylinder.body.apply_impulse_at_local_point((impulse,0))
	total.append(impulse)
	# run simulation
	while running and tick < 200:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-60)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-40)
		tick += 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		if STAT_FRICTION != None:
		# static friction for all bodies
			if (cylinder.body.velocity == (0,0)):
				cylinder.body.update_velocity(cylinder.body, (0,0), STAT_FRICTION, 1/50.0)
			if (cone.body.velocity == (0,0)):
				cone.body.update_velocity(cone.body, (0,0), STAT_FRICTION, 1/50.0)
			if (ball.body.velocity == (0,0)):
				ball.body.update_velocity(ball.body, (0,0), STAT_FRICTION, 1/50.0)
		
		print "Velocity: ", cylinder.body.velocity[0]#, "Time: ", tick
		print "Distance: ", cylinder.body.position[0] - 300
		print "Force: ", cylinder.body.force

		dist.append(cylinder.body.velocity[0]/50.0)

		# set clock
		clock = pygame.time.Clock()
		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			screen.blit(fireSprite, pBall)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)
	
	# remove value from collision list
	try:
		handlers.collision = []
	except:
		print "Exited before collision."

	# output to user and return tuple
	print "Total impulse: ", sum(total)
	print sum(dist)

def sim1(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Simulation of Cylinder pushing Cone into Fireball from a short distance
	away. Originally to be compared with longDistanceSim in Moral Kinematics.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 1: Sim 1")
	
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
	ball = agents.fireball(900, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(600, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(300, 300, AP_MASS)
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

	# animation flag and counter
	x = 0
	cnt = 0

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-60)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		tick += 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# static friction for all bodies
		if (cylinder.body.velocity[0] == (0,0)):
			cylinder.body.update_velocity(cylinder.body, (0,0), STAT_FRICTION, 1/50.0)
		if (cone.body.velocity == (0,0)):
			cone.body.update_velocity(cone.body, (0,0), STAT_FRICTION, 1/50.0)
		if (ball.body.velocity == (0,0)):
			ball.body.update_velocity(ball.body, (0,0), STAT_FRICTION, 1/50.0)
		
		# keep the Agent at it's intended velocity for some duration
		if (cylinder.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		elif (len(handlers.collision) == 1):
			imp = cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((-1*imp,0))
			total.append(math.fabs(imp))

		# append positional values to each list
		xImpsAgent.append(cylinder.body.position[0])
		yImpsAgent.append(cylinder.body.position[1])
		xImpsPatient.append(cone.body.position[0])
		yImpsPatient.append(cone.body.position[1])
		xImpsFireball.append(ball.body.position[0])
		yImpsFireball.append(ball.body.position[1])

		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			setBackground(screen)
			screen.blit(fireSprite, pBall)
			screen.blit(patientSprite, pCone)
			screen.blit(agentSprite, pAgent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)

	# patient collision
	for i in range(25):
		screen.fill((255,255,255))
		space.debug_draw(options)
		setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		if (cnt < 12 and x == 0):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt += 1
			if cnt == 12:
				x = 1
				cnt = 11
		elif (cnt >= 0 and x == 1):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt -= 1
		else:
			screen.blit(fireSprite, pBall)
			screen.blit(agentSprite, pAgent)

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# output to user and return tuple
	print "Total impulse: ", sum(total)
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def sim2(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Simulation of Cylinder pushing Cone into Fireball from a short distance
	away. Originally to be compared with longDistanceSim in Moral Kinematics.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 1: Sim 1")
	
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
	ball = agents.fireball(900, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(600, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(100, 300, AP_MASS)
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

	# animation flag and counter
	x = 0
	cnt = 0

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-60)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		tick += 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# static friction for all bodies
		if (cylinder.body.velocity[0] == (0,0)):
			cylinder.body.update_velocity(cylinder.body, (0,0), STAT_FRICTION, 1/50.0)
		if (cone.body.velocity == (0,0)):
			cone.body.update_velocity(cone.body, (0,0), STAT_FRICTION, 1/50.0)
		if (ball.body.velocity == (0,0)):
			ball.body.update_velocity(ball.body, (0,0), STAT_FRICTION, 1/50.0)
		
		# keep the Agent at it's intended velocity for some duration
		if (cylinder.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		elif (len(handlers.collision) == 1):
			imp = cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((-1*imp,0))
			total.append(math.fabs(imp))

		# append positional values to each list
		xImpsAgent.append(cylinder.body.position[0])
		yImpsAgent.append(cylinder.body.position[1])
		xImpsPatient.append(cone.body.position[0])
		yImpsPatient.append(cone.body.position[1])
		xImpsFireball.append(ball.body.position[0])
		yImpsFireball.append(ball.body.position[1])

		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			setBackground(screen)
			screen.blit(fireSprite, pBall)
			screen.blit(patientSprite, pCone)
			screen.blit(agentSprite, pAgent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)

	# patient collision
	for i in range(25):
		screen.fill((255,255,255))
		space.debug_draw(options)
		setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		if (cnt < 12 and x == 0):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt += 1
			if cnt == 12:
				x = 1
				cnt = 11
		elif (cnt >= 0 and x == 1):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt -= 1
		else:
			screen.blit(fireSprite, pBall)
			screen.blit(agentSprite, pAgent)

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# output to user and return tuple
	print "Total impulse: ", sum(total)
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def agentPush(space, screen, options, guess=False, impulse=AGENT_WALKING):
	'''
	Simulation of Cylinder pushing Cone into Fireball from a short distance
	away. Originally to be compared with longDistanceSim in Moral Kinematics.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 1: Agent Push")
	
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
	ball = agents.fireball(800, 220, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(300, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(800, 400, AP_MASS)
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
	time = 160

	# animation flag and counter
	x = 0
	cnt = 0

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-60)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		tick += 1
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# static friction for all bodies
		if (cylinder.body.velocity[0] == (0,0)):
			cylinder.body.update_velocity(cylinder.body, (0,0), STAT_FRICTION, 1/50.0)
		if (cone.body.velocity == (0,0)):
			cone.body.update_velocity(cone.body, (0,0), STAT_FRICTION, 1/50.0)
		if (ball.body.velocity == (0,0)):
			ball.body.update_velocity(ball.body, (0,0), STAT_FRICTION, 1/50.0)
		
		# keep the Agent at it's intended velocity for some duration
		if (cone.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cone.body.velocity[0]
			cone.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		elif (len(handlers.collision) == 1):
			imp = cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((-1*imp,0))
			total.append(math.fabs(imp))
		if (time == 0):
			cylinder.body.apply_impulse_at_local_point((0,-1*AGENT_RUNNING))

		# append positional values to each list
		xImpsAgent.append(cylinder.body.position[0])
		yImpsAgent.append(cylinder.body.position[1])
		xImpsPatient.append(cone.body.position[0])
		yImpsPatient.append(cone.body.position[1])
		xImpsFireball.append(ball.body.position[0])
		yImpsFireball.append(ball.body.position[1])

		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			setBackground(screen)
			screen.blit(fireSprite, pBall)
			screen.blit(patientSprite, pCone)
			screen.blit(agentSprite, pAgent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)

	# patient collision
	for i in range(25):
		screen.fill((255,255,255))
		space.debug_draw(options)
		setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		if (cnt < 12 and x == 0):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt += 1
			if cnt == 12:
				x = 1
				cnt = 11
		elif (cnt >= 0 and x == 1):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt -= 1
		else:
			screen.blit(fireSprite, pBall)
			screen.blit(agentSprite, pAgent)

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# output to user and return tuple
	print "Total impulse: ", sum(total)
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def agentTap(space, screen, options, guess=False, impulse=AGENT_WALKING):
	'''
	Simulation of Cylinder pushing Cone into Fireball from a short distance
	away. Originally to be compared with longDistanceSim in Moral Kinematics.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 1: Agent Push")
	
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
	ball = agents.fireball(900, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(800, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(750, 300, AP_MASS)
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
	time = 160

	# animation flag and counter
	x = 0
	cnt = 0

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-60)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		tick += 1
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# static friction for all bodies
		if (cylinder.body.velocity[0] == (0,0)):
			cylinder.body.update_velocity(cylinder.body, (0,0), STAT_FRICTION, 1/50.0)
		if (cone.body.velocity == (0,0)):
			cone.body.update_velocity(cone.body, (0,0), STAT_FRICTION, 1/50.0)
		if (ball.body.velocity == (0,0)):
			ball.body.update_velocity(ball.body, (0,0), STAT_FRICTION, 1/50.0)
		
		# keep the Agent at it's intended velocity for some duration
		if (cylinder.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cone.body.velocity[0]
			cone.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		elif (len(handlers.collision) == 1):
			imp = cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((-1*imp,0))
			total.append(math.fabs(imp))

		# append positional values to each list
		xImpsAgent.append(cylinder.body.position[0])
		yImpsAgent.append(cylinder.body.position[1])
		xImpsPatient.append(cone.body.position[0])
		yImpsPatient.append(cone.body.position[1])
		xImpsFireball.append(ball.body.position[0])
		yImpsFireball.append(ball.body.position[1])

		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			setBackground(screen)
			screen.blit(fireSprite, pBall)
			screen.blit(patientSprite, pCone)
			screen.blit(agentSprite, pAgent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)

	# patient collision
	for i in range(25):
		screen.fill((255,255,255))
		space.debug_draw(options)
		setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		if (cnt < 12 and x == 0):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt += 1
			if cnt == 12:
				x = 1
				cnt = 11
		elif (cnt >= 0 and x == 1):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt -= 1
		else:
			screen.blit(fireSprite, pBall)
			screen.blit(agentSprite, pAgent)

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# output to user and return tuple
	print "Total impulse: ", sum(total)
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def noTouch(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Simulation of Cylinder pushing Cone into Fireball from a short distance
	away. Originally to be compared with longDistanceSim in Moral Kinematics.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 1: Agent Push")
	
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
	ball = agents.fireball(900, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(300, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(600, 400, AP_MASS)
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
	time = 160

	# animation flag and counter
	x = 0
	cnt = 0

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-60)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		tick += 1
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# static friction for all bodies
		if (cylinder.body.velocity[0] == (0,0)):
			cylinder.body.update_velocity(cylinder.body, (0,0), STAT_FRICTION, 1/50.0)
		if (cone.body.velocity == (0,0)):
			cone.body.update_velocity(cone.body, (0,0), STAT_FRICTION, 1/50.0)
		if (ball.body.velocity == (0,0)):
			ball.body.update_velocity(ball.body, (0,0), STAT_FRICTION, 1/50.0)
		
		# keep the Agent at it's intended velocity for some duration
		if (cone.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cone.body.velocity[0]
			cone.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		elif (len(handlers.collision) == 1):
			imp = cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((-1*imp,0))
			total.append(math.fabs(imp))

		# append positional values to each list
		xImpsAgent.append(cylinder.body.position[0])
		yImpsAgent.append(cylinder.body.position[1])
		xImpsPatient.append(cone.body.position[0])
		yImpsPatient.append(cone.body.position[1])
		xImpsFireball.append(ball.body.position[0])
		yImpsFireball.append(ball.body.position[1])

		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			setBackground(screen)
			screen.blit(fireSprite, pBall)
			screen.blit(patientSprite, pCone)
			screen.blit(agentSprite, pAgent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)

	# patient collision
	for i in range(25):
		screen.fill((255,255,255))
		space.debug_draw(options)
		setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		if (cnt < 12 and x == 0):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt += 1
			if cnt == 12:
				x = 1
				cnt = 11
		elif (cnt >= 0 and x == 1):
			img = pygame.image.load(ani[cnt])
			screen.blit(img, pCone)
			cnt -= 1
		else:
			screen.blit(fireSprite, pBall)
			screen.blit(agentSprite, pAgent)

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# output to user and return tuple
	print "Total impulse: ", sum(total)
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)