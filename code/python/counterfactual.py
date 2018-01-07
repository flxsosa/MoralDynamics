'''
Counterfactual Simulations for Moral Dynamics

Januaray 6, 2018
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
# Length, in ticks, of counterfactual simulation after critical point
length_of_counterfactual = 150

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
	# Set title of simulation display
	pygame.display.set_caption("Simulation 1: Short Distance v1")
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 9
	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = 0
	factual_impulse_fireball = 0

	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2

	# dynamic friction
	space.damping = DYN_FRICTION
	
	# add shapes besides Agent
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(800, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)
			screen.blit(patientSprite, position_patient)
			#screen.blit(agentSprite, position_agent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)

	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(100):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		# position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))
		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)
			screen.blit(patientSprite, position_patient)
			#screen.blit(agentSprite, position_agent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)
	if (len(handlers.PF_COLLISION) > 0):
		collision = True
	else:
		collision = False

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# Return counterfactual result
	print(collision)
	return (collision)

# No Counterfactual
def medium_distance_v1(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Agent pushes Patient into Fireball from a medium distance away.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set simulation display title
	pygame.display.set_caption("Medium Distance v1")
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 0

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
	while running and len(handlers.collision) == 0:
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
	
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
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
	# Simulation tick at which Agent factually collides with Patient
	pygame.display.set_caption("Simulation 3: Long Distance v1")
	
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 109
	
	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = 0
	factual_impulse_fireball = 0

	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2

	# dynamic friction
	space.damping = DYN_FRICTION
	
	# add shapes besides Agent
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(800, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)
			screen.blit(patientSprite, position_patient)
			#screen.blit(agentSprite, position_agent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)

	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(100):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		# position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))
		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)
			screen.blit(patientSprite, position_patient)
			#screen.blit(agentSprite, position_agent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)

	if (len(handlers.PF_COLLISION) > 0):
		collision = True
	else:
		collision = False

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# Return counterfactual result
	print(collision)
	return (collision)

def static(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Patient bounces off of Agent and then falls into a Fireball.
	
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 4: Static")
	
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 54
	
	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = AGENT_RUNNING
	factual_impulse_fireball = 0

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
	fireball = agents.fireball(750, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(300, 360, AP_MASS)
	space.add(patient.body, patient.shape)
	running = True
	tick = 0
	count = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1
		
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Patient at it's intended velocity for some duration
		if (patient.body.velocity[0] < impulse and patient.body.velocity[1] < AGENT_RUNNING and \
				len(handlers.collision) == 0):
			impx = impulse - patient.body.velocity[0]
			impy = AGENT_WALKING - patient.body.velocity[1]
			patient.body.apply_impulse_at_local_point((impx,0))

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

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)	
	
	# Run counterfactual
	for i in range(100):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))
		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)
			screen.blit(patientSprite, position_patient)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)
		
	if (len(handlers.PF_COLLISION) > 0):
		collision = True
	else:
		collision = False
	
	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
		handlers.totalImpulse = []
	except:
		print("Exited before collision.")

	# Return counterfactual result
	print(collision)
	return (collision)

def slow_collision(space, screen, options, guess=False, impulse=AGENT_WALKING):
	'''
	Patient gets hit by Agent and then runs slower than before being hit.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 5: Slow Collision")
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 17

	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = 0
	factual_impulse_fireball = 0

	# set up collision handlers
	ch0 = space.add_collision_handler(0,2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0,1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(500,300, AP_MASS)
	space.add(patient.body, patient.shape)

	running = True
	tick = 0
	count = 0
	time = 50

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		tick+=1
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

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

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)	
	
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(100):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))
		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)
			screen.blit(patientSprite, position_patient)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)
	
	if (len(handlers.PF_COLLISION) > 0):
		collision = True
	else:
		collision = False

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# Return counterfactual result
	print(collision)
	return (collision)

def fast_collision(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Patient gets hit by Agent and then runs faster than before being hit.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 6: Fast Collision")
	
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 9

	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = 0
	factual_impulse_fireball = 0

	# set up collision handlers
	ch0 = space.add_collision_handler(0,2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0,1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(500,300, AP_MASS)
	space.add(patient.body, patient.shape)

	running = True
	tick = 0
	count = 0
	time = 50

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		tick+=1
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

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

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)	
	
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(100):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))
		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)
			screen.blit(patientSprite, position_patient)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)
	
	if (len(handlers.PF_COLLISION) > 0):
		collision = True
	else:
		collision = False

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# Return counterfactual result
	print(collision)
	return (collision)

def dodge(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Agent dodges Patient as Patient runs towards Fireball.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 7: Dodge")
	
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 40

	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = AGENT_RUNNING
	factual_impulse_fireball = 0

	# set up collision handlers
	ch0 = space.add_collision_handler(0,2)
	ch0.data["surface"] = screen
	ch0.begin = handlers.rem2
	ch0.post_solve = handlers.rem0
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(100, 300, AP_MASS)
	space.add(patient.body, patient.shape)

	running = True
	tick = 0
	time = 75

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		tick+=1
		time-=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep Patient at it's intended velocity
		if (patient.body.velocity[0] < AGENT_RUNNING):
			imp = AGENT_RUNNING - patient.body.velocity[0]
			patient.body.apply_impulse_at_local_point((imp,0))

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

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)	
	
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(150):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))
		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)
			screen.blit(patientSprite, position_patient)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)
	
	if (len(handlers.PF_COLLISION) > 0):
		collision = True
	else:
		collision = False

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# Return counterfactual result
	print(collision)
	return (collision)

def double_push(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Agent pushes Patient twice into Fireball.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 8: Double Push")
	
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 9

	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = 0
	factual_impulse_fireball = 0

	# set up collision handlers
	ch0 = space.add_collision_handler(0,2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(200, 300, AP_MASS)
	space.add(patient.body, patient.shape)

	running = True
	tick = 0
	time = 100

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		tick+=1
		time -= 1
		
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

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

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)	

	# Run counterfactual
	for i in range(150):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))
		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)
			screen.blit(patientSprite, position_patient)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)
	
	if (len(handlers.PF_COLLISION) > 0):
		collision = True
	else:
		collision = False

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# Return counterfactual result
	print(collision)
	return (collision)

def medium_push(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Agent pushes Patient into Fireball over a medium distance into Fireball.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 9: Medium Push")
	
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 59

	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = 0
	factual_impulse_fireball = 0

	# set up collision handlers
	ch0 = space.add_collision_handler(0,1)
	ch0.data["surface"] = screen
	ch0.begin = handlers.rem2
	ch0.post_solve = handlers.rem0
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(500, 300, AP_MASS)
	space.add(patient.body, patient.shape)

	running = True
	tick = 0
	time = 70

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		
		time -= 1
		tick+=1
		
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

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

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)	
	
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(length_of_counterfactual):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))
		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)
			screen.blit(patientSprite, position_patient)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)
	
	if (len(handlers.PF_COLLISION) > 0):
		collision = True
	else:
		collision = False

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# Return counterfactual result
	print(collision)
	return (collision)

def long_push(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Agent pushes Patient into Fireball over long distance into Fireball.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 10: Long Push")
	
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 9

	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = 0
	factual_impulse_fireball = 0

	# set up collision handlers
	ch0 = space.add_collision_handler(0,1)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch0.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)	
	patient = agents.patient(200, 300, AP_MASS)
	space.add(patient.body, patient.shape)	

	running = True
	tick = 0
	time = 100

	# animation flag and counter 
	x = 0
	cnt = 0

	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		time -= 1
		tick+=1
		
		# allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

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

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)	
	
	# Run counterfactual
	for i in range(length_of_counterfactual):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))
		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)
			screen.blit(patientSprite, position_patient)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)
	
	if (len(handlers.PF_COLLISION) > 0):
		collision = True
	else:
		collision = False

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."
	
	# Return counterfactual result
	print(collision)
	return (collision)

# No Counterfactual
def push_fireball(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Agent pushes Fireball into Patient.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	if(not guess):
		pygame.display.set_caption("Push Fireball")
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 0
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
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
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
	pygame.display.set_caption("Simulation 2: Medium Distance v2")
	
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 59

	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = 0
	factual_impulse_fireball = 0

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
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(500, 300, AP_MASS)
	space.add(patient.body, patient.shape)

	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)
			screen.blit(patientSprite, position_patient)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)
	
	# Run counterfactual
	for i in range(length_of_counterfactual):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))
		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)
			screen.blit(patientSprite, position_patient)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)
	
	if (len(handlers.PF_COLLISION) > 0):
		collision = True
	else:
		collision = False

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."
	
	# Return counterfactual result
	print(collision)
	return (collision)
# No Counterfactual
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
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 0

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
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
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
	pygame.display.set_caption("Simulation 12: No Touch")
	
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 0

	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = AGENT_RUNNING
	factual_impulse_fireball = 0

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
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(100, 300, AP_MASS)
	space.add(patient.body, patient.shape)

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
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		tick+=1
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (patient.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - patient.body.velocity[0]
			patient.body.apply_impulse_at_local_point((imp,0))
		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)
			screen.blit(patientSprite, position_patient)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)
	
	if (len(handlers.PF_COLLISION) > 0):
		collision = True
	else:
		collision = False
		
	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

	# Return counterfactual result
	print(collision)
	return (collision)

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
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 122

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
	while running and len(handlers.collision) == 0:
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
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
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
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 122

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
	while running and len(handlers.collision) == 0:
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
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
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
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 73

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
	while running and len(handlers.collision) == 0:
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
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
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
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 67

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
	while running and len(handlers.collision) == 0:
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
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
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
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 73

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
	while running and len(handlers.collision) == 0:
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
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
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
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 67

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
	while running and len(handlers.collision) == 0:
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
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
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
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 122

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
	while running and len(handlers.collision) == 0:
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
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
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
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 122

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
	while running and len(handlers.collision) == 0:
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
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
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

# Dynamics simulations

def sim_1_patient(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 109

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
	while running and len(handlers.collision) == 0:
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
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
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
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 109

	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(2, 1)
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
	while running and len(handlers.collision) == 0:
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
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
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
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 64

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
	while running and len(handlers.collision) == 0:
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
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
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
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 64

	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(2, 1)
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
	while running and len(handlers.collision) == 0:
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
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
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
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 84

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
	while running and len(handlers.collision) == 0:
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
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
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
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 84

	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(2, 1)
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
	while running and len(handlers.collision) == 0:
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
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
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
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 67

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
	while running and len(handlers.collision) == 0:
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
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
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
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 67

	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(2, 1)
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
	while running and len(handlers.collision) == 0:
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
	point_of_collision = tick
	print "Point of collision occurs at tick {0}".format(point_of_collision)
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

# Counterfactual Simulations

def counterfactual_short_distance(space, screen, options, impulse=AGENT_RUNNING):
	'''
	Counterfactual simulation of Agent pushing Patient into Fireball from a short distance
	away. 
	Originally to be compared with longDistanceSim in Moral Kinematics.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set caption
	pygame.display.set_caption("Counterfactual Simulation: Short Distance v1")

	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2

	# Dynamic friction for simulation
	space.damping = DYN_FRICTION
	
	# Add shapes
	fireball = agents.fireball(900, 300, F_MASS)
	patient = agents.patient(800, 300, AP_MASS)
	agent = agents.agent(200, 300, AP_MASS)
	space.add(agent.body, agent.shape)
	
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

	# Animation flag and counter
	x = 0
	cnt = 0

	# Pause before showing clip
	helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1

	# Set game clock
	clock = pygame.time.Clock()

	# Run simulation
	while running and tick < 34:
		# Update fireball sprite according to object's position
		pAgent = (agent.body.position[0]-30,agent.body.position[1]-30)
		tick+=1

		# Allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (agent.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)

		# append positional values to each list
		xImpsAgent.append(agent.body.position[0])
		yImpsAgent.append(agent.body.position[1])
	
		# setup display and run sim based on whether it's truth or guess	
		# draw screen
		screen.fill((255,255,255))
		space.debug_draw(options)
		helper.setBackground(screen)
		screen.blit(agentSprite, pAgent)

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)

		# update pymunk space
		space.step(1/50.0)

	# Run counterfactual
	for i in range(100):
		# Update fireball sprite according to object's position
		pAgent = (agent.body.position[0]-30,agent.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1

		# Allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (agent.body.velocity[0] < impulse): #and len(handlers.collision) == 0):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,helper.sample_trajectory()*impulse))
			total.append(imp)

		# append positional values to each list
		xImpsAgent.append(agent.body.position[0])
		yImpsAgent.append(agent.body.position[1])

		# draw screen
		screen.fill((255,255,255))
		space.debug_draw(options)
		helper.setBackground(screen)
		screen.blit(agentSprite, pAgent)

		# adjust pygame screen and move clock forward
		pygame.display.flip()
		clock.tick(50)

		# update pymunk space
		space.step(1/50.0)

	print "Collision at tick = {0}".format(tick)
	
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