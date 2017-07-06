'''
Simulations for Moral Dynamics

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
import glob
import helper

# MODEL PARAMETERS
DYN_FRICTION = 0.6
AP_MASS = 1
F_MASS = 1
AGENT_RUNNING = 300
AGENT_WALKING = 150

# SPRITES
fireSprite = pygame.image.load("Sprites/firea.png")
patientSprite = pygame.image.load("Sprites/Patient.png")
agentSprite = pygame.image.load("Sprites/Agent.png")

# PATIENT-AGENT ANIMATION SPRITES
ani = glob.glob("Sprites/fireball*.png")
ani.sort()

# Experiment 2 simulations

def shortDistancev1(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	cylinder = agents.agent(700, 300, AP_MASS)
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

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		helper.snapshot(screen, tick)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
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
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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

def mediumDistancev1(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	cylinder = agents.agent(500, 300, AP_MASS)
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

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		helper.snapshot(screen, tick)
		tick+=1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

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
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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

def longDistancev1(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		helper.snapshot(screen, tick)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

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
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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
	ball = agents.fireball(750, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(300, 360, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(650, 400, AP_MASS)
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

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		helper.snapshot(screen, tick)
		tick+=1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Patient at it's intended velocity for some duration
		if (cone.body.velocity[0] < impulse and cone.body.velocity[1] < AGENT_RUNNING and \
				len(handlers.collision) == 0):
			impx = impulse - cone.body.velocity[0]
			impy = AGENT_WALKING - cone.body.velocity[1]
			cone.body.apply_impulse_at_local_point((impx,0))

			# if 	collision between agent and patient, have agent push back once
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
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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

def slowCollision(space, screen, options, guess=False, impulse=AGENT_WALKING):
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
	cone = agents.patient(500,300, AP_MASS)
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
	time = 50

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		helper.snapshot(screen, tick)
		tick+=1
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at their intended velocity for some duration
		if (cylinder.body.velocity[0] < impulse and time > 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)

		# when Agent and Patient collide, have Patient push back and Agent stop
		if (time == 0):
			count+=1
			#cone.body.apply_impulse_at_local_point((-100,0))
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
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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
	cone = agents.patient(500, 300, AP_MASS)
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
	time = 25

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		helper.snapshot(screen, tick)
		tick+=1
		time -= 1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep Agent and Patient at their intended velocities
		if (cylinder.body.velocity[0] < impulse and time > 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		
		# when Agent and Patient collide, have Patient push back and Agent stop
		if (time == 0):
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
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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
	cone = agents.patient(100, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(500, 300, AP_MASS)
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
	time = 75

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		helper.snapshot(screen, tick)
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
		if (time == 22):
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
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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

def doublePush(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	time = 100

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		helper.snapshot(screen, tick)
		tick+=1
		time -= 1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep Agent at intended velocity
		if (time > 90 and cylinder.body.velocity[0] < impulse):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		elif(time < 89 and time > 0):
			if (cylinder.body.velocity[0] != 0):
				imp = cylinder.body.velocity[0]
				cylinder.body.apply_impulse_at_local_point((-1*imp,0))
				total.append(imp)
		elif(len(handlers.PF_COLLISION) == 0 and cylinder.body.velocity[0] < impulse):
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
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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
	cone = agents.patient(500, 300, AP_MASS)
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
	time = 70

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		time -= 1
		helper.snapshot(screen, tick)
		tick+=1
		
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep Agent at intended velocity
		if (len(handlers.PF_COLLISION) == 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(math.fabs(imp))

		# when t == 0, have Agent stop 
		#if (time == 0):
		#	cylinder.body.apply_impulse_at_local_point((-1*cylinder.body.velocity[0],0))
		
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
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		time -= 1
		helper.snapshot(screen, tick)
		tick+=1
		
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep Agent at intended velocity
		if (len(handlers.PF_COLLISION) == 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(math.fabs(imp))

		# when t == 0, have Agent stop 
		#if (time == 0):
		#	cylinder.body.apply_impulse_at_local_point((-1*cylinder.body.velocity[0],0))
		
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
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		time -= 1
		helper.snapshot(screen, tick)
		tick+=1
		
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep Agent at intended velocity
		if (len(handlers.PF_COLLISION) == 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(math.fabs(imp))

		# when t == 0, have Agent stop 
		#if (time == 0):
		#	cylinder.body.apply_impulse_at_local_point((-1*cylinder.body.velocity[0],0))
		
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
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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

def mediumDistancev2(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	cone = agents.patient(500, 300, AP_MASS)
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

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		helper.snapshot(screen, tick)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

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
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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

def longDistancev2(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	cylinder = agents.agent(-100, 300, AP_MASS)
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

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		helper.snapshot(screen, tick)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
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
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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
	cone = agents.patient(100, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(500, 400, AP_MASS)
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

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		helper.snapshot(screen, tick)
		tick+=1
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

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
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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

# Experiment 1 simulations

def victim_moving_moving(space, screen, options, guess=False, impulse=AGENT_WALKING):
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
	ball = agents.fireball(100, 250, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(800, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(500, 400, AP_MASS)
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
	time = 50

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		helper.snapshot(screen, tick)
		tick+=1
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (ball.body.velocity[0] < AGENT_WALKING):
			imp = AGENT_WALKING - ball.body.velocity[0]
			ball.body.apply_impulse_at_local_point((imp,0))
		if (math.fabs(cone.body.velocity[0]) < AGENT_WALKING and len(handlers.collision) == 0):
			imp = AGENT_RUNNING - math.fabs(cone.body.velocity[0])
			cone.body.apply_impulse_at_local_point((-1*imp, 0))
		if (time == 0):
			cylinder.body.apply_impulse_at_local_point((0,-1*impulse))
			total.append(impulse)

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
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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

def victim_moving_static(space, screen, options, guess=False, impulse=AGENT_WALKING):
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
	ball = agents.fireball(400, 250, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(800, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(500, 400, AP_MASS)
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
	time = 50

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		helper.snapshot(screen, tick)
		tick+=1
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(cone.body.velocity[0]) < AGENT_WALKING and len(handlers.collision) == 0):
			imp = AGENT_RUNNING - math.fabs(cone.body.velocity[0])
			cone.body.apply_impulse_at_local_point((-1*imp, 0))
		if (time == 0):
			cylinder.body.apply_impulse_at_local_point((0,-1*impulse))
			total.append(impulse)

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
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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

def victim_static_moving(space, screen, options, guess=False, impulse=AGENT_WALKING):
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
	ch1 = space.add_collision_handler(2, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2

	# dynamic friction
	space.damping = DYN_FRICTION
	
	# add shapes
	ball = agents.fireball(800, 200, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(350, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(350, 400, AP_MASS)
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
	time = 30

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		helper.snapshot(screen, tick)
		tick+=1
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(ball.body.velocity[0]) < AGENT_RUNNING):# and len(handlers.collision) == 0):
			imp = AGENT_RUNNING - math.fabs(ball.body.velocity[0])
			ball.body.apply_impulse_at_local_point((-1*imp, 0))
		if (time == 0):
			cylinder.body.apply_impulse_at_local_point((0,-1*impulse))
			total.append(impulse)

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
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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

def victim_static_static(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	ball = agents.fireball(800, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(500, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(200, 300, AP_MASS)
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
	time = 50

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		helper.snapshot(screen, tick)
		tick+=1
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
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

		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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

def harm_static_moving(space, screen, options, guess=False, impulse=AGENT_WALKING):
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
	ch1 = space.add_collision_handler(2, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2

	# dynamic friction
	space.damping = DYN_FRICTION
	
	# add shapes
	ball = agents.fireball(350, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(800, 200, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(350, 400, AP_MASS)
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
	time = 30

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		helper.snapshot(screen, tick)
		tick+=1
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(cone.body.velocity[0]) < AGENT_RUNNING and len(handlers.collision) == 0):
			imp = AGENT_RUNNING - math.fabs(cone.body.velocity[0])
			cone.body.apply_impulse_at_local_point((-1*imp, 0))
		if (time == 0):
			cylinder.body.apply_impulse_at_local_point((0,-1*impulse))
			total.append(impulse)

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
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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

def harm_static_static(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	ch1 = space.add_collision_handler(2, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2

	# dynamic friction
	space.damping = DYN_FRICTION
	
	# add shapes
	ball = agents.fireball(500, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(800, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(200, 300, AP_MASS)
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
	time = 50

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		helper.snapshot(screen, tick)
		tick+=1
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
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

		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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

def harm_moving_static(space, screen, options, guess=False, impulse=AGENT_WALKING):
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
	ch1 = space.add_collision_handler(2, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2

	# dynamic friction
	space.damping = DYN_FRICTION
	
	# add shapes
	ball = agents.fireball(800, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(400, 250, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(500, 400, AP_MASS)
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
	time = 50

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		helper.snapshot(screen, tick)
		tick+=1
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(ball.body.velocity[0]) < AGENT_WALKING and len(handlers.collision) == 0):
			imp = AGENT_RUNNING - math.fabs(cone.body.velocity[0])
			ball.body.apply_impulse_at_local_point((-1*imp, 0))
		if (time == 0):
			cylinder.body.apply_impulse_at_local_point((0,-1*impulse))
			total.append(impulse)

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
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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

def harm_moving_moving(space, screen, options, guess=False, impulse=AGENT_WALKING):
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
	ch1 = space.add_collision_handler(2, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2

	# dynamic friction
	space.damping = DYN_FRICTION
	
	# add shapes
	ball = agents.fireball(800, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(100, 250, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(500, 400, AP_MASS)
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
	time = 50

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		helper.snapshot(screen, tick)
		tick+=1
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (cone.body.velocity[0] < AGENT_WALKING):
			imp = AGENT_WALKING - cone.body.velocity[0]
			cone.body.apply_impulse_at_local_point((imp,0))
		if (math.fabs(ball.body.velocity[0]) < AGENT_WALKING and len(handlers.collision) == 0):
			imp = AGENT_RUNNING - math.fabs(ball.body.velocity[0])
			ball.body.apply_impulse_at_local_point((-1*imp, 0))
		if (time == 0):
			cylinder.body.apply_impulse_at_local_point((0,-1*impulse))
			total.append(impulse)

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
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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
		helper.snapshot(screen, tick)
		tick+=1
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

# Instruction simulations for experiments on mTurk

def patientWalksToFireball(space, screen, options, guess=False, impulse=AGENT_WALKING):
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
	ball = agents.fireball(600, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(200, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	
	# lists for impulses per timestep, total impulses, running flag, and ticks
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
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		helper.snapshot(screen, tick)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (cone.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cone.body.velocity[0]
			cone.body.apply_impulse_at_local_point((imp,0))
		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, pBall)
			screen.blit(patientSprite, pCone)

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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)
		helper.snapshot(screen, tick)
		tick+=1
	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def agentWalksToFireball(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 1: Short Distance")
	
	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0

	# dynamic friction
	space.damping = DYN_FRICTION
	
	# add shapes
	ball = agents.fireball(600, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cylinder = agents.agent(200, 300, AP_MASS)
	space.add(cylinder.body, cylinder.shape)
	
	# lists for impulses per timestep, total impulses, running flag, and ticks
	running = True
	tick = 0
	time = 100

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and time!=0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		helper.snapshot(screen, tick)
		tick += 1
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (cylinder.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, pBall)
			screen.blit(agentSprite, pCone)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def fireballMoving(space, screen, options, guess=False, impulse=AGENT_WALKING):
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
	ball = agents.fireball(300, 300, F_MASS)
	space.add(ball.body, ball.shape)
	
	# lists for impulses per timestep, total impulses, running flag, and ticks
	running = True
	tick = 0
	time = 100

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and time!=0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		time -= 1
		helper.snapshot(screen, tick)
		tick+=1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (ball.body.velocity[0] < impulse):
			imp = impulse - ball.body.velocity[0]
			ball.body.apply_impulse_at_local_point((imp,0))
		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, pBall)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def agentSavesPatient(space, screen, options, guess=False, impulse=AGENT_WALKING):
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
	cone = agents.patient(400, 300, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(750, 400, AP_MASS)
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
	time = 100
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		time-=1
		helper.snapshot(screen, tick)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (cone.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cone.body.velocity[0]
			cone.body.apply_impulse_at_local_point((imp,0))

		if (time == 0):
			cylinder.body.apply_impulse_at_local_point((0,-1*AGENT_WALKING))

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
			helper.setBackground(screen)
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
		helper.setBackground(screen)
		screen.blit(fireSprite, pBall)
		screen.blit(agentSprite, pAgent)

		# conditional animation sequence
		screen.blit(patientSprite, pCone)
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