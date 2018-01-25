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
# Dyanmic friction value
DYN_FRICTION = 0.6
# Mass of Patient and Agent
AP_MASS = 1
# Mass of Fireball
F_MASS = 1
# Velocity of a given agent running or walking
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

def short_distance_v1(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Agent pushes Patient into Fireball from a short distance away.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 1: Short Distance v1")
	
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
		#helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
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
		#helper.snapshot(screen, tick)
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

def medium_distance_v1(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Agent pushes Patient into Fireball from a medium distance away.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Medium Distance v1")

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
		#helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
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
		#helper.snapshot(screen, tick)
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

def long_distance_v1(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Agent pushes Patient into Fireball from a long distance away.
	
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 3: Long Distance v1")

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
		#helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
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
		#helper.snapshot(screen, tick)
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
	Patient bounces off of Agent and then falls into a Fireball.
	
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	if (not guess):
		pygame.display.set_caption("Simulation 4: Static")

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
		#helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
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
		#helper.snapshot(screen, tick)
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

def slow_collision(space, screen, options, guess=False, impulse=AGENT_WALKING):
	'''
	Patient gets hit by Agent and then runs slower than before being hit.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	if(not guess):
		pygame.display.set_caption("Simulation 5: Slow Collision")

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
		#helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
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
		#helper.snapshot(screen, tick)
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

def fast_collision(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Patient gets hit by Agent and then runs faster than before being hit.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	if(not guess):
		pygame.display.set_caption("Simulation 6: Fast Collision")

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
		#helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
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
		#helper.snapshot(screen, tick)
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
	Agent dodges Patient as Patient runs towards Fireball.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	TODO:
	1. See if there's a better way to deal with the time variable
	'''
	if(not guess):
		pygame.display.set_caption("Simulation 7: Dodge")
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
		#helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
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
		#helper.snapshot(screen, tick)
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

def double_push(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Agent pushes Patient twice into Fireball.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	if(not guess):
		pygame.display.set_caption("Simulation 8: Double Push")

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
		#helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
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
		#helper.snapshot(screen, tick)
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

def medium_push(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Agent pushes Patient into Fireball over a medium distance into Fireball.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	TODO:
	1. Make pushing not time dependent but distance dependent
	'''
	if(not guess):
		pygame.display.set_caption("Simulation 9: Medium Push")
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
		#helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		time -= 1
		#helper.snapshot(screen, tick)
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
		#helper.snapshot(screen, tick)
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

def long_push(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Agent pushes Patient into Fireball over long distance into Fireball.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	if(not guess):
		pygame.display.set_caption("Simulation 10: Long Push")
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
		#helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		time -= 1
		#helper.snapshot(screen, tick)
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
		#helper.snapshot(screen, tick)
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

def push_fireball(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Agent pushes Fireball into Patient.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	if(not guess):
		pygame.display.set_caption("Push Fireball")
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
		#helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		time -= 1
		#helper.snapshot(screen, tick)
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
		#helper.snapshot(screen, tick)
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

def medium_distance_v2(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Agent pushes Patient into Fireball from a medium distance away.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 2: Medium Distance v2")
	
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
		#helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
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
		#helper.snapshot(screen, tick)
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

def long_distance_v2(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Agent pushes Patient into Fireball from a long distance away.
	
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Long Distance v2")
	
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
		#helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
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
		#helper.snapshot(screen, tick)
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

def no_touch(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Agent watces Patient run into Fireball wihtout intervening.
	
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 12: No Touch")
	
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
		#helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
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
		#helper.snapshot(screen, tick)
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

def victim_moving_moving(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Fireball moving right from upper left corner. Patient moving left from lower 
	right corner. Agent rests in lower middle of screen. 
	Agent pushes moving Patient into moving Fireball when Patient
	comes in proximity of Agent.
	
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 13: Victim Moving, Harm Moving")
	
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
	ball = agents.fireball(100, 200, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(800, 400, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(500, 500, AP_MASS)
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
	time = 89

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
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
			imp = AGENT_WALKING - math.fabs(cone.body.velocity[0])
			cone.body.apply_impulse_at_local_point((-1*imp, 0))
		if (time <= 0 and cylinder.body.velocity[1] < impulse):
			imp = impulse - math.fabs(cylinder.body.velocity[1])
			cylinder.body.apply_impulse_at_local_point((0,-1*imp))
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
		#helper.snapshot(screen, tick)
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

def victim_moving_static(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Fireball rests in upper left of screen. Patient moving left from lower 
	right corner. Agent rests in lower middle of screen. 
	Agent pushes moving Patient into resting Fireball when Patient
	comes in proximity of Agent.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 14: Victim Moving, Harm Static")
	
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
	ball = agents.fireball(450, 200, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(800, 400, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(500, 500, AP_MASS)
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
	time = 89

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
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
			imp = AGENT_WALKING - math.fabs(cone.body.velocity[0])
			cone.body.apply_impulse_at_local_point((-1*imp, 0))
		if (time <= 0 and math.fabs(cylinder.body.velocity[1]) < impulse):
			imp = impulse - math.fabs(cylinder.body.velocity[1])
			cylinder.body.apply_impulse_at_local_point((0,-1*imp))
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
		#helper.snapshot(screen, tick)
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

def victim_static_moving(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Fireball moving left from upper right corner. Patient rests in front of Agent in
	lower middle of screen. Agent rests behind Patient in lower middle of screen. 
	Agent pushes resting Patient into moving Fireball when Fireball
	comes in proximity of Patient.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 15: Victim Static, Harm Moving")
	
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
	cone = agents.patient(350, 400, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(350, 500, AP_MASS)
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
	time = 40

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
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
		if (time <= 0 and math.fabs(cylinder.body.velocity[1]) < impulse):
			imp = impulse - math.fabs(cylinder.body.velocity[1])
			cylinder.body.apply_impulse_at_local_point((0,-1*imp))
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
		#helper.snapshot(screen, tick)
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
	Agent rests on left side of screen. Fireball rests on right side of screen.
	Patient rests in between Agent and Fireball. 
	Agent pushes resting Patient into resting Fireball.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 16: Victim Static, Harm Static")
	
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
		#helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (cylinder.body.velocity[0] < impulse):
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
		#helper.snapshot(screen, tick)
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

def harm_static_moving(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Patient moving left from upper right corner. Fireball rests in front of Agent in
	lower middle of screen. Agent rests behind Fireball in lower middle of screen. 
	Agent pushes resting Fireball into moving Patient when Patient comes in proximity 
	of Patient.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 19: Harm Static, Victim Moving")
	
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
	ball = agents.fireball(350, 400, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(800, 200, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(350, 500, AP_MASS)
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
	time = 40

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(cone.body.velocity[0]) < AGENT_RUNNING):# and len(handlers.collision) == 0):
			imp = AGENT_RUNNING - math.fabs(cone.body.velocity[0])
			cone.body.apply_impulse_at_local_point((-1*imp, 0))
		if (time <= 0 and math.fabs(cylinder.body.velocity[1]) < impulse):
			imp = impulse - math.fabs(cylinder.body.velocity[1])
			cylinder.body.apply_impulse_at_local_point((0,-1*imp))
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
		#helper.snapshot(screen, tick)
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
	Agent rests on left side of screen. Patient rests on right side of screen.
	Fireball rests in between Agent and Patient. 
	Agent pushes resting Fireball into resting Patient.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 20: Harm Static, Victim Static")
	
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
		#helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (cylinder.body.velocity[0] < impulse):
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
		#helper.snapshot(screen, tick)
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

def harm_moving_static(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Patient rests in upper left of screen. Fireball moving left from lower 
	right corner. Agent rests in lower middle of screen. 
	Agent pushes moving Fireball into resting Patient when Fireball
	comes in proximity of Agent.
	
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 18: Harm Moving, Victim Static")
	
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
	ball = agents.fireball(800, 400, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(450, 200, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(500, 500, AP_MASS)
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
	time = 89

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
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
			imp = AGENT_WALKING - math.fabs(ball.body.velocity[0])
			ball.body.apply_impulse_at_local_point((-1*imp, 0))
		if (time <= 0 and math.fabs(cylinder.body.velocity[1]) < impulse):
			imp = impulse - math.fabs(cylinder.body.velocity[1])
			cylinder.body.apply_impulse_at_local_point((0,-1*imp))
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
		#helper.snapshot(screen, tick)
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

def harm_moving_moving(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Patient moving right from upper left corner. Fireball moving left from lower 
	right corner. Agent rests in lower middle of screen. 
	Agent pushes moving Fireball into moving Patient when Fireball
	comes in proximity of Agent.
	
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 17: Harm Moving, Victim Moving")
	
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
	ball = agents.fireball(800, 400, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(100, 200, AP_MASS)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(500, 500, AP_MASS)
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
	time = 89

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-25)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
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
			imp = AGENT_WALKING - math.fabs(ball.body.velocity[0])
			ball.body.apply_impulse_at_local_point((-1*imp,0))
		if (cone.body.velocity[0] < AGENT_WALKING):
			imp = AGENT_WALKING - cone.body.velocity[0]
			cone.body.apply_impulse_at_local_point((imp, 0))
		if (time <= 0 and cylinder.body.velocity[1] < impulse):
			imp = impulse - math.fabs(cylinder.body.velocity[1])
			cylinder.body.apply_impulse_at_local_point((0,-1*imp))
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
		#helper.snapshot(screen, tick)
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

def patient_walks_to_fireball(space, screen, options, guess=False, impulse=AGENT_WALKING):
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
		#helper.snapshot(screen, tick)
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
		#helper.snapshot(screen, tick)
		tick+=1
	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def agent_walks_to_fireball(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
		#helper.snapshot(screen, tick)
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

def fireball_moving(space, screen, options, guess=False, impulse=AGENT_WALKING):
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
		#helper.snapshot(screen, tick)
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

def agent_saves_patient(space, screen, options, guess=False, impulse=AGENT_WALKING):
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
		#helper.snapshot(screen, tick)
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

# Dynamics simulations

def sim_1_patient(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	cone = agents.patient(400, 300, AP_MASS)
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
		#helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (cylinder.body.velocity[0] < impulse):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		if (cone.body.velocity[0] < AGENT_WALKING):
			imp = AGENT_WALKING - cone.body.velocity[0]
			cone.body.apply_impulse_at_local_point((imp,0))

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
		#helper.snapshot(screen, tick)
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

def sim_1_fireball(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	ball = agents.fireball(400, 300, F_MASS)
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
	total = []
	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (cylinder.body.velocity[0] < impulse):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		if (ball.body.velocity[0] < AGENT_WALKING):
			imp = AGENT_WALKING - ball.body.velocity[0]
			ball.body.apply_impulse_at_local_point((imp,0))

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
		#helper.snapshot(screen, tick)
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

def sim_2_patient(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (cylinder.body.velocity[0] < impulse):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		if (math.fabs(cone.body.velocity[0]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(cone.body.velocity[0])
			cone.body.apply_impulse_at_local_point((-1*imp,0))

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
		#helper.snapshot(screen, tick)
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

def sim_2_fireball(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	ball = agents.fireball(500, 300, F_MASS)
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
	total = []
	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (cylinder.body.velocity[0] < impulse):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		if (math.fabs(ball.body.velocity[0]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(ball.body.velocity[0])
			ball.body.apply_impulse_at_local_point((-1*imp,0))

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
		#helper.snapshot(screen, tick)
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

def sim_3_patient(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	ball = agents.fireball(800, 300, F_MASS)
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

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (cylinder.body.velocity[0] < impulse):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		if (math.fabs(ball.body.velocity[0]) < AGENT_WALKING):
			imp = math.fabs(ball.body.velocity[0]) - AGENT_WALKING
			ball.body.apply_impulse_at_local_point((imp,0))

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
		#helper.snapshot(screen, tick)
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

def sim_3_fireball(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	ball = agents.fireball(500, 300, F_MASS)
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
		#helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (cylinder.body.velocity[0] < impulse):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		if (math.fabs(cone.body.velocity[0]) < AGENT_WALKING):
			imp = math.fabs(cone.body.velocity[0]) - AGENT_WALKING
			cone.body.apply_impulse_at_local_point((imp,0))

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
		#helper.snapshot(screen, tick)
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

def sim_4_patient(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	ball = agents.fireball(700, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(400, 300, AP_MASS)
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
	time=40

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		time-=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (cylinder.body.velocity[0] < impulse):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		if (time < 0 and math.fabs(ball.body.velocity[0]) < AGENT_WALKING):
			imp = math.fabs(ball.body.velocity[0]) - AGENT_WALKING
			ball.body.apply_impulse_at_local_point((-1*imp,0))

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
		#helper.snapshot(screen, tick)
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

def sim_4_fireball(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	ball = agents.fireball(400, 300, F_MASS)
	space.add(ball.body, ball.shape)
	cone = agents.patient(700, 300, AP_MASS)
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
	time = 40

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, cylinder, ball, cone)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
		pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
		pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		time-=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (cylinder.body.velocity[0] < impulse):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		if (time < 0 and math.fabs(cone.body.velocity[0]) < AGENT_WALKING):
			imp = math.fabs(cone.body.velocity[0]) - AGENT_WALKING
			cone.body.apply_impulse_at_local_point((-1*imp,0))

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
		#helper.snapshot(screen, tick)
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

# Good scenarios

def agent_saves_patient_1(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(2, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(100, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(900, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(700, 100, AP_MASS)
	space.add(agent.body, agent.shape)

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
	time = 160

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30, agent.body.position[1]-30)
		tick+=1
		time-=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (time < 0 and math.fabs(agent.body.velocity[1]) < impulse and 
			len(handlers.collision) == 0):
			imp = impulse - math.fabs(agent.body.velocity[1])
			agent.body.apply_impulse_at_local_point((0,imp))
			total.append(imp)
		elif(math.fabs(agent.body.velocity[0]) > 0 or math.fabs(agent.body.velocity[1]) > 0):
			impx = agent.body.velocity[0]*-1
			impy = agent.body.velocity[1]*-1
			agent.body.apply_impulse_at_local_point((impx,impy))
		if (math.fabs(fireball.body.velocity[0]) < AGENT_WALKING):
			imp = math.fabs(fireball.body.velocity[0]) - AGENT_WALKING
			fireball.body.apply_impulse_at_local_point((-1*imp,0))

		# append positional values to each list
		xImpsAgent.append(agent.body.position[0])
		yImpsAgent.append(agent.body.position[1])
		xImpsPatient.append(patient.body.position[0])
		yImpsPatient.append(patient.body.position[1])
		xImpsFireball.append(fireball.body.position[0])
		yImpsFireball.append(fireball.body.position[1])

		# set clock
		clock = pygame.time.Clock()

		# setup display and run sim based on whether it's truth or guess
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)
			screen.blit(patientSprite, position_patient)
			screen.blit(agentSprite, position_agent)

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
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def agent_makes_patient_safer(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(2, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(350, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(450, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(450, 100, AP_MASS)
	space.add(agent.body, agent.shape)

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
	time = 160

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30, agent.body.position[1]-30)
		tick+=1
		time-=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(agent.body.velocity[1]) < impulse and 
			len(handlers.collision) == 0):
			imp = impulse - math.fabs(agent.body.velocity[1])
			agent.body.apply_impulse_at_local_point((-6,imp))
			total.append(imp)
		elif(math.fabs(agent.body.velocity[0]) > 0 or math.fabs(agent.body.velocity[1]) > 0):
			impx = agent.body.velocity[0]*-1
			impy = agent.body.velocity[1]*-1
			agent.body.apply_impulse_at_local_point((impx,impy))


		# append positional values to each list
		xImpsAgent.append(agent.body.position[0])
		yImpsAgent.append(agent.body.position[1])
		xImpsPatient.append(patient.body.position[0])
		yImpsPatient.append(patient.body.position[1])
		xImpsFireball.append(fireball.body.position[0])
		yImpsFireball.append(fireball.body.position[1])

		# set clock
		clock = pygame.time.Clock()

		# setup display and run sim based on whether it's truth or guess
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)
			screen.blit(patientSprite, position_patient)
			screen.blit(agentSprite, position_agent)

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
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def agent_saves_patient_2(space, screen, options, guess=False, impulse=AGENT_WALKING):
	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(100, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(700, 300, AP_MASS)
	space.add(agent.body, agent.shape)

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
	time = 40

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30, agent.body.position[1]-30)
		tick+=1
		time-=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(patient.body.velocity[0]) < impulse and 
			len(handlers.collision) == 0):
			imp = impulse - math.fabs(patient.body.velocity[0])
			patient.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		if (time < 0 and math.fabs(agent.body.velocity[0]) < AGENT_RUNNING and 
			len(handlers.collision) == 0):
			imp = impulse - math.fabs(agent.body.velocity[0])
			agent.body.apply_impulse_at_local_point((-1*imp,0))
			total.append(imp)
		elif(math.fabs(agent.body.velocity[0]) > 0 or math.fabs(agent.body.velocity[1]) > 0):
			impx = agent.body.velocity[0]*-1
			impy = agent.body.velocity[1]*-1
			agent.body.apply_impulse_at_local_point((impx,impy))

		# append positional values to each list
		xImpsAgent.append(agent.body.position[0])
		yImpsAgent.append(agent.body.position[1])
		xImpsPatient.append(patient.body.position[0])
		yImpsPatient.append(patient.body.position[1])
		xImpsFireball.append(fireball.body.position[0])
		yImpsFireball.append(fireball.body.position[1])

		# set clock
		clock = pygame.time.Clock()

		# setup display and run sim based on whether it's truth or guess
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)
			screen.blit(patientSprite, position_patient)
			screen.blit(agentSprite, position_agent)

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
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def dodge_save(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Agent dodges Patient as Patient runs towards Fireball.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	TODO:
	1. See if there's a better way to deal with the time variable
	'''
	if(not guess):
		pygame.display.set_caption("Simulation 7: Dodge")
	# set up collision handlers
	ch0 = space.add_collision_handler(0,2)
	ch0.data["surface"] = screen
	ch0.begin = handlers.rem2
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(100, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(500, 200, AP_MASS)
	space.add(agent.body, agent.shape)

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
	helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		time-=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep Patient at it's intended velocity
		if (patient.body.velocity[0] < AGENT_RUNNING and len(handlers.collision) == 0):
			imp = AGENT_RUNNING - patient.body.velocity[0]
			patient.body.apply_impulse_at_local_point((imp,0))
		elif(math.fabs(agent.body.velocity[0]) > 0 or math.fabs(agent.body.velocity[1]) > 0):
			impx = agent.body.velocity[0]*-1
			impy = agent.body.velocity[1]*-1
			agent.body.apply_impulse_at_local_point((impx,impy))

		# at t == 20, Agent dogdes Patient
		if (time == 40):
			agent.body.apply_impulse_at_local_point((0,impulse))
			total.append(impulse)
		if (time == 22):
			imp = agent.body.velocity[1]
			agent.body.apply_impulse_at_local_point((0,-1*imp))
			total.append(math.fabs(imp))

		# append positional values to each list
		xImpsAgent.append(agent.body.position[0])
		yImpsAgent.append(agent.body.position[1])
		xImpsPatient.append(patient.body.position[0])
		yImpsPatient.append(patient.body.position[1])
		xImpsFireball.append(fireball.body.position[0])
		yImpsFireball.append(fireball.body.position[1])

		# set clock
		clock = pygame.time.Clock()

		# setup display and run sim based on whether it's truth or guess
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)
			screen.blit(patientSprite, position_patient)
			screen.blit(agentSprite, position_agent)

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
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick: ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)