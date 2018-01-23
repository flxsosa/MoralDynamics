import pymunk
import pygame
import agents
import handlers
import math
import pymunk.pygame_util
from pygame.locals import *
import glob
import helper
import json
import sys

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

# Dictionary for json file, used for each simulation
sim_dict = {}

path = '../data/'

# Experiment 2 simulations

def short_distance_v1(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	'''
	Agent pushes Patient into Fireball from a short distance away.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(800, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(700, 300, AP_MASS)
	space.add(agent.body, agent.shape)
	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (agent.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			
		elif (len(handlers.collision) == 1):
			imp = agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((-1*imp,0))
			
		
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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	
	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def medium_distance_v1(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	'''
	Agent pushes Patient into Fireball from a medium distance away.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(800, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(500, 300, AP_MASS)
	space.add(agent.body, agent.shape)
	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (agent.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			
		if (len(handlers.collision) == 1):
			imp = agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((-1*imp,0))
			

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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	
	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."	

def long_distance_v1(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	'''
	Agent pushes Patient into Fireball from a long distance away.
	
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''

	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	patient = agents.patient(800, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(100, 300, AP_MASS)
	space.add(agent.body, agent.shape)
	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30, agent.body.position[1]-30)
		
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (agent.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
		if (len(handlers.collision) == 1):
			imp = agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((-1*imp,0))

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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	
	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."	

def static(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	'''
	Patient bounces off of Agent and then falls into a Fireball.
	
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(750, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(300, 360, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(650, 400, AP_MASS)
	space.add(agent.body, agent.shape)
	running = True
	tick = 0
	count = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

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

			# if collision between agent and patient, have agent push back once
		if (len(handlers.collision) != 0 and count==0):
			count+=1
			try:
				agent.body.apply_impulse_at_local_point((handlers.totalImpulse[0][0], 
					handlers.totalImpulse[0][1]))

			except:
				pass

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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
		handlers.totalImpulse = []
	except:
		print("Exited before collision.")

def slow_collision(space, screen, options, guess=True, impulse=AGENT_WALKING):
	'''
	Patient gets hit by Agent and then runs slower than before being hit.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(500,300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(400, 300, AP_MASS)
	space.add(agent.body, agent.shape)
	running = True
	tick = 0
	count = 0
	time = 50

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at their intended velocity for some duration
		if (agent.body.velocity[0] < impulse and time > 0):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			

		# when Agent and Patient collide, have Patient push back and Agent stop
		if (time == 0):
			count+=1
			agent.body.apply_impulse_at_local_point((-1*agent.body.velocity[0],0))

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
		
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def fast_collision(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	'''
	Patient gets hit by Agent and then runs faster than before being hit.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(500, 300, AP_MASS)
	space.add(patient.body, patient.shape)	
	agent = agents.agent(400, 300, AP_MASS)
	space.add(agent.body, agent.shape)
	running = True
	tick = 0
	time = 25

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep Agent and Patient at their intended velocities
		if (agent.body.velocity[0] < impulse and time > 0):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			
		
		# when Agent and Patient collide, have Patient push back and Agent stop
		if (time == 0):
			agent.body.apply_impulse_at_local_point((-1*agent.body.velocity[0],0))

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
		
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def dodge(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	'''
	Agent dodges Patient as Patient runs towards Fireball.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

	if(not guess):
		pygame.display.set_caption("Simulation 7: Dodge")
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
	agent = agents.agent(500, 300, AP_MASS)
	space.add(agent.body, agent.shape)
	running = True
	tick = 0
	time = 75

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
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

		# at t == 20, Agent dogdes Patient
		if (time == 40):
			agent.body.apply_impulse_at_local_point((0,impulse))

		if (time == 22):
			imp = agent.body.velocity[1]
			agent.body.apply_impulse_at_local_point((0,-1*imp))
			

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
		
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def double_push(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	'''
	Agent pushes Patient twice into Fireball.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(200, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(100, 300, AP_MASS)
	space.add(agent.body, agent.shape)
	running = True
	tick = 0
	time = 100

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		time -= 1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep Agent at intended velocity
		if (time > 90 and agent.body.velocity[0] < impulse):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			
		elif(time < 89 and time > 0):
			if (agent.body.velocity[0] != 0):
				imp = agent.body.velocity[0]
				agent.body.apply_impulse_at_local_point((-1*imp,0))
				
		elif(len(handlers.PF_COLLISION) == 0 and agent.body.velocity[0] < impulse):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			

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
		
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def medium_push(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	'''
	Agent pushes Patient into Fireball over a medium distance into Fireball.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

	if(not guess):
		pygame.display.set_caption("Simulation 9: Medium Push")
	# set up collision handlers
	ch0 = space.add_collision_handler(0,2)
	ch0.data["surface"] = screen
	ch0.begin = handlers.rem2
	ch0.post_solve = handlers.rem0
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(500, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(100, 300, AP_MASS)
	space.add(agent.body, agent.shape)

	running = True
	tick = 0
	time = 70

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		time -= 1
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep Agent at intended velocity
		if (len(handlers.PF_COLLISION) == 0):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			

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
		
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def long_push(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	'''
	Agent pushes Patient into Fireball over long distance into Fireball.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

	if(not guess):
		pygame.display.set_caption("Simulation 10: Long Push")
	# set up collision handlers
	ch0 = space.add_collision_handler(0,2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch0.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(200, 300, AP_MASS)
	space.add(patient.body, patient.shape)	
	agent = agents.agent(100, 300, AP_MASS)
	space.add(agent.body, agent.shape)

	running = True
	tick = 0
	time = 100

	# animation flag and counter 
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		time -= 1
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep Agent at intended velocity
		if (len(handlers.PF_COLLISION) == 0):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			

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
		
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def push_fireball(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	'''
	Agent pushes Fireball into Patient.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(200, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(900, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(100, 300, AP_MASS)
	space.add(agent.body, agent.shape)

	running = True
	tick = 0
	time = 100

	# animation flag and counter 
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		time -= 1
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep Agent at intended velocity
		if (len(handlers.PF_COLLISION) == 0):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			

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
		
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def medium_distance_v2(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	'''
	Agent pushes Patient into Fireball from a medium distance away.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(500, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(100, 300, AP_MASS)
	space.add(agent.body, agent.shape)
	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (agent.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			
		elif (len(handlers.collision) == 1):
			imp = agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((-1*imp,0))
			
		
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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def long_distance_v2(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	'''
	Agent pushes Patient into Fireball from a long distance away.
	
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(600, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(-100, 300, AP_MASS)
	space.add(agent.body, agent.shape)
	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (agent.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			
		elif (len(handlers.collision) == 1):
			imp = agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((-1*imp,0))
			
		
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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def no_touch(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	'''
	Agent watces Patient run into Fireball wihtout intervening.
	
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(100, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(500, 400, AP_MASS)
	space.add(agent.body, agent.shape)
	running = True
	tick = 0
	time = 160

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
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
			screen.blit(agentSprite, position_agent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."


# Experiment 1 simulations

def victim_moving_moving(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	'''
	Fireball moving right from upper left corner. Patient moving left from lower 
	right corner. Agent rests in lower middle of screen. 
	Agent pushes moving Patient into moving Fireball when Patient
	comes in proximity of Agent.
	
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(100, 200, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(800, 400, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(500, 500, AP_MASS)
	space.add(agent.body, agent.shape)
	running = True
	tick = 0
	time = 89

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0]-30, 'y' : agent.body.position[1]-30})
		patient_position_dict.append({'x' : patient.body.position[0]-30, 'y' : patient.body.position[1]-30})
		fireball_position_dict.append({'x' : fireball.body.position[0]-30, 'y' : fireball.body.position[1]-23})

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0]-30, 'y' : agent.body.position[1]-30})
		patient_position_dict.append({'x' : patient.body.position[0]-30, 'y' : patient.body.position[1]-30})
		fireball_position_dict.append({'x' : fireball.body.position[0]-30, 'y' : fireball.body.position[1]-23})
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (fireball.body.velocity[0] < AGENT_WALKING):
			imp = AGENT_WALKING - fireball.body.velocity[0]
			fireball.body.apply_impulse_at_local_point((imp,0))
		if (math.fabs(patient.body.velocity[0]) < AGENT_WALKING and len(handlers.collision) == 0):
			imp = AGENT_WALKING - math.fabs(patient.body.velocity[0])
			patient.body.apply_impulse_at_local_point((-1*imp, 0))
		if (time <= 0 and agent.body.velocity[1] < impulse):
			imp = impulse - math.fabs(agent.body.velocity[1])
			agent.body.apply_impulse_at_local_point((0,-1*imp))
			
		
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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def victim_moving_static(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	'''
	Fireball rests in upper left of screen. Patient moving left from lower 
	right corner. Agent rests in lower middle of screen. 
	Agent pushes moving Patient into resting Fireball when Patient
	comes in proximity of Agent.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(450, 200, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(800, 400, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(500, 500, AP_MASS)
	space.add(agent.body, agent.shape)
	running = True
	tick = 0
	time = 89

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0]-30, 'y' : agent.body.position[1]-30})
		patient_position_dict.append({'x' : patient.body.position[0]-30, 'y' : patient.body.position[1]-30})
		fireball_position_dict.append({'x' : fireball.body.position[0]-30, 'y' : fireball.body.position[1]-25})

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0]-30, 'y' : agent.body.position[1]-30})
		patient_position_dict.append({'x' : patient.body.position[0]-30, 'y' : patient.body.position[1]-30})
		fireball_position_dict.append({'x' : fireball.body.position[0]-30, 'y' : fireball.body.position[1]-25})
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(patient.body.velocity[0]) < AGENT_WALKING and len(handlers.collision) == 0):
			imp = AGENT_WALKING - math.fabs(patient.body.velocity[0])
			patient.body.apply_impulse_at_local_point((-1*imp, 0))
		if (time <= 0 and math.fabs(agent.body.velocity[1]) < impulse):
			imp = impulse - math.fabs(agent.body.velocity[1])
			agent.body.apply_impulse_at_local_point((0,-1*imp))
			
		
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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def victim_static_moving(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	'''
	Fireball moving left from upper right corner. Patient rests in front of Agent in
	lower middle of screen. Agent rests behind Patient in lower middle of screen. 
	Agent pushes resting Patient into moving Fireball when Fireball
	comes in proximity of Patient.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(800, 200, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(350, 400, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(350, 500, AP_MASS)
	space.add(agent.body, agent.shape)
	running = True
	tick = 0
	time = 40

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(fireball.body.velocity[0]) < AGENT_RUNNING):# and len(handlers.collision) == 0):
			imp = AGENT_RUNNING - math.fabs(fireball.body.velocity[0])
			fireball.body.apply_impulse_at_local_point((-1*imp, 0))
		if (time <= 0 and math.fabs(agent.body.velocity[1]) < impulse):
			imp = impulse - math.fabs(agent.body.velocity[1])
			agent.body.apply_impulse_at_local_point((0,-1*imp))
			
		
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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def victim_static_static(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	'''
	Agent rests on left side of screen. Fireball rests on right side of screen.
	Patient rests in between Agent and Fireball. 
	Agent pushes resting Patient into resting Fireball.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(800, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(500, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(200, 300, AP_MASS)
	space.add(agent.body, agent.shape)
	running = True
	tick = 0
	time = 50

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0]-30, 'y' : agent.body.position[1]-30})
		patient_position_dict.append({'x' : patient.body.position[0]-30, 'y' : patient.body.position[1]-30})
		fireball_position_dict.append({'x' : fireball.body.position[0]-35, 'y' : fireball.body.position[1]-30})

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0]-30, 'y' : agent.body.position[1]-30})
		patient_position_dict.append({'x' : patient.body.position[0]-30, 'y' : patient.body.position[1]-30})
		fireball_position_dict.append({'x' : fireball.body.position[0]-35, 'y' : fireball.body.position[1]-30})
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (agent.body.velocity[0] < impulse):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			

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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def harm_static_moving(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	'''
	Patient moving left from upper right corner. Fireball rests in front of Agent in
	lower middle of screen. Agent rests behind Fireball in lower middle of screen. 
	Agent pushes resting Fireball into moving Patient when Patient comes in proximity 
	of Patient.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(350, 400, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(800, 200, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(350, 500, AP_MASS)
	space.add(agent.body, agent.shape)
	running = True
	tick = 0
	time = 40

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(patient.body.velocity[0]) < AGENT_RUNNING):# and len(handlers.collision) == 0):
			imp = AGENT_RUNNING - math.fabs(patient.body.velocity[0])
			patient.body.apply_impulse_at_local_point((-1*imp, 0))
		if (time <= 0 and math.fabs(agent.body.velocity[1]) < impulse):
			imp = impulse - math.fabs(agent.body.velocity[1])
			agent.body.apply_impulse_at_local_point((0,-1*imp))
			
		
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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def harm_static_static(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	'''
	Agent rests on left side of screen. Patient rests on right side of screen.
	Fireball rests in between Agent and Patient. 
	Agent pushes resting Fireball into resting Patient.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(500, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(800, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(200, 300, AP_MASS)
	space.add(agent.body, agent.shape)
	running = True
	tick = 0
	time = 50

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0]-30, 'y' : agent.body.position[1]-30})
		patient_position_dict.append({'x' : patient.body.position[0]-35, 'y' : patient.body.position[1]-30})
		fireball_position_dict.append({'x' : fireball.body.position[0]-30, 'y' : fireball.body.position[1]-30})

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0]-30, 'y' : agent.body.position[1]-30})
		patient_position_dict.append({'x' : patient.body.position[0]-35, 'y' : patient.body.position[1]-30})
		fireball_position_dict.append({'x' : fireball.body.position[0]-30, 'y' : fireball.body.position[1]-30})
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (agent.body.velocity[0] < impulse):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			
		
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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def harm_moving_static(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	'''
	Patient rests in upper left of screen. Fireball moving left from lower 
	right corner. Agent rests in lower middle of screen. 
	Agent pushes moving Fireball into resting Patient when Fireball
	comes in proximity of Agent.
	
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(800, 400, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(450, 200, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(500, 500, AP_MASS)
	space.add(agent.body, agent.shape)
	running = True
	tick = 0
	time = 89

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0]-30, 'y' : agent.body.position[1]-30})
		patient_position_dict.append({'x' : patient.body.position[0]-30, 'y' : patient.body.position[1]-25})
		fireball_position_dict.append({'x' : fireball.body.position[0]-30, 'y' : fireball.body.position[1]-30})

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0]-30, 'y' : agent.body.position[1]-30})
		patient_position_dict.append({'x' : patient.body.position[0]-30, 'y' : patient.body.position[1]-25})
		fireball_position_dict.append({'x' : fireball.body.position[0]-30, 'y' : fireball.body.position[1]-30})
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(fireball.body.velocity[0]) < AGENT_WALKING and len(handlers.collision) == 0):
			imp = AGENT_WALKING - math.fabs(fireball.body.velocity[0])
			fireball.body.apply_impulse_at_local_point((-1*imp, 0))
		if (time <= 0 and math.fabs(agent.body.velocity[1]) < impulse):
			imp = impulse - math.fabs(agent.body.velocity[1])
			agent.body.apply_impulse_at_local_point((0,-1*imp))
			
		
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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def harm_moving_moving(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	'''
	Patient moving right from upper left corner. Fireball moving left from lower 
	right corner. Agent rests in lower middle of screen. 
	Agent pushes moving Fireball into moving Patient when Fireball
	comes in proximity of Agent.
	
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

	# if it's a truth sim, we use a display
	if(not guess):
		pygame.display.set_caption("Simulation 17: Harm Moving, Victim Moving")
	
	# set up collision handlers
	# ch0 = space.add_collision_handler(0, 2)
	# ch0.data["surface"] = screen
	# ch0.post_solve = handlers.rem0
	# ch1 = space.add_collision_handler(2, 1)
	# ch1.data["surface"] = screen
	# ch1.begin = handlers.rem2
	ch0 = space.add_collision_handler(2, 0)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(2, 1)
	ch1.data["surface"] = screen
	ch1.post_solve = handlers.rem2

	# dynamic friction
	space.damping = DYN_FRICTION
	
	# add shapes
	fireball = agents.fireball(800, 400, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(100, 200, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(500, 500, AP_MASS)
	space.add(agent.body, agent.shape)
	running = True
	tick = 0
	time = 89

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0]-30, 'y' : agent.body.position[1]-30})
		patient_position_dict.append({'x' : patient.body.position[0]-30, 'y' : patient.body.position[1]-23})
		fireball_position_dict.append({'x' : fireball.body.position[0]-30, 'y' : fireball.body.position[1]-30})

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0],fireball.body.position[1])
		position_patient = (patient.body.position[0],patient.body.position[1])
		position_agent = (agent.body.position[0],agent.body.position[1])
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0]-30, 'y' : agent.body.position[1]-30})
		patient_position_dict.append({'x' : patient.body.position[0]-30, 'y' : patient.body.position[1]-23})
		fireball_position_dict.append({'x' : fireball.body.position[0]-30, 'y' : fireball.body.position[1]-30})
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(fireball.body.velocity[0]) < AGENT_WALKING and len(handlers.collision) == 0):
			imp = AGENT_WALKING - math.fabs(fireball.body.velocity[0])
			fireball.body.apply_impulse_at_local_point((-1*imp,0))
		if (patient.body.velocity[0] < AGENT_WALKING):
			imp = AGENT_WALKING - patient.body.velocity[0]
			patient.body.apply_impulse_at_local_point((imp, 0))
		if (time <= 0 and agent.body.velocity[1] < impulse):
			imp = impulse - math.fabs(agent.body.velocity[1])
			agent.body.apply_impulse_at_local_point((0,-1*imp))
			

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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."


# Instruction simulations for experiments on mTurk

def patient_walks_to_fireball(space, screen, options, guess=True, impulse=AGENT_WALKING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(600, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(200, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : -300, 'y' : -300})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def agent_walks_to_fireball(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0

	# dynamic friction
	space.damping = DYN_FRICTION
	
	# add shapes
	fireball = agents.fireball(600, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	agent = agents.agent(200, 300, AP_MASS)
	space.add(agent.body, agent.shape)
	running = True
	tick = 0
	time = 100

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and time!=0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : -300, 'y' : -300})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
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
		if (agent.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)
			screen.blit(agentSprite, position_agent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def fireball_moving(space, screen, options, guess=True, impulse=AGENT_WALKING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(300, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	running = True
	tick = 0
	time = 100

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and time!=0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		time -= 1
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : -300, 'y' : -300})
		patient_position_dict.append({'x' : -300, 'y' : -300})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		
		# keep the Agent at it's intended velocity for some duration
		if (fireball.body.velocity[0] < impulse):
			imp = impulse - fireball.body.velocity[0]
			fireball.body.apply_impulse_at_local_point((imp,0))
		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def agent_saves_patient(space, screen, options, guess=True, impulse=AGENT_WALKING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	patient = agents.patient(400, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(750, 400, AP_MASS)
	space.add(agent.body, agent.shape)
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
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		time-=1
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

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

		if (time == 0):
			agent.body.apply_impulse_at_local_point((0,-1*AGENT_WALKING))
		
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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."


# Dynamics simulations

def sim_1_patient(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	patient = agents.patient(400, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(100, 300, AP_MASS)
	space.add(agent.body, agent.shape)

	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (agent.body.velocity[0] < impulse):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			
		if (patient.body.velocity[0] < AGENT_WALKING):
			imp = AGENT_WALKING - patient.body.velocity[0]
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
			screen.blit(agentSprite, position_agent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)	

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def sim_1_fireball(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(400, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(900, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(100, 300, AP_MASS)
	space.add(agent.body, agent.shape)

	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (agent.body.velocity[0] < impulse):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			
		if (fireball.body.velocity[0] < AGENT_WALKING):
			imp = AGENT_WALKING - fireball.body.velocity[0]
			fireball.body.apply_impulse_at_local_point((imp,0))

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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def sim_2_patient(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	patient = agents.patient(500, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(100, 300, AP_MASS)
	space.add(agent.body, agent.shape)

	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (agent.body.velocity[0] < impulse):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			
		if (math.fabs(patient.body.velocity[0]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(patient.body.velocity[0])
			patient.body.apply_impulse_at_local_point((-1*imp,0))

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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def sim_2_fireball(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(500, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(900, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(100, 300, AP_MASS)
	space.add(agent.body, agent.shape)

	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (agent.body.velocity[0] < impulse):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			
		if (math.fabs(fireball.body.velocity[0]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(fireball.body.velocity[0])
			fireball.body.apply_impulse_at_local_point((-1*imp,0))

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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def sim_3_patient(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(800, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(500, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(100, 300, AP_MASS)
	space.add(agent.body, agent.shape)

	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (agent.body.velocity[0] < impulse):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			
		if (math.fabs(fireball.body.velocity[0]) < AGENT_WALKING):
			imp = math.fabs(fireball.body.velocity[0]) - AGENT_WALKING
			fireball.body.apply_impulse_at_local_point((imp,0))

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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def sim_3_fireball(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(500, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(800, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(100, 300, AP_MASS)
	space.add(agent.body, agent.shape)
	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (agent.body.velocity[0] < impulse):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			
		if (math.fabs(patient.body.velocity[0]) < AGENT_WALKING):
			imp = math.fabs(patient.body.velocity[0]) - AGENT_WALKING
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
			screen.blit(agentSprite, position_agent)

			# adjust pygame screen and move clock forward
			pygame.display.flip()
			clock.tick(50)
		else:
			clock.tick(500000)

		# update pymunk space
		space.step(1/50.0)	

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def sim_4_patient(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(700, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(400, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(100, 300, AP_MASS)
	space.add(agent.body, agent.shape)

	running = True
	tick = 0
	time=40

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		#helper.snapshot(screen, tick)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		time-=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (agent.body.velocity[0] < impulse):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			
		if (time < 0 and math.fabs(fireball.body.velocity[0]) < AGENT_WALKING):
			imp = math.fabs(fireball.body.velocity[0]) - AGENT_WALKING
			fireball.body.apply_impulse_at_local_point((-1*imp,0))

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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."

def sim_4_fireball(space, screen, options, guess=True, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(400, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(700, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(100, 300, AP_MASS)
	space.add(agent.body, agent.shape)

	running = True
	tick = 0
	time = 40

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		time-=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (agent.body.velocity[0] < impulse):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			
		if (time < 0 and math.fabs(patient.body.velocity[0]) < AGENT_WALKING):
			imp = math.fabs(patient.body.velocity[0]) - AGENT_WALKING
			patient.body.apply_impulse_at_local_point((-1*imp,0))

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

	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)

	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."
