import pymunk
import pygame
import agents
import handlers
import math
import pymunk.pygame_util
from pygame.locals import *
import glob
import helper
import sys
import json

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

sim_dict = {}

path = "../data/"

# +cause, good, fireball, low effort
def good_1(space, screen, options, guess=False, impulse=AGENT_WALKING):
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
	ch1 = space.add_collision_handler(2, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(100, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(900, 300, AP_MASS)
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
	count = 250

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		tick+=1
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})

	# run simulation
	while running and count > 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30, agent.body.position[1]-30)
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1
		time-=1
		count-=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(fireball.body.velocity[0]) < impulse and 
			len(handlers.collision) == 0):
			imp = impulse - math.fabs(fireball.body.velocity[0])
			fireball.body.apply_impulse_at_local_point((imp,0))
		if(math.fabs(agent.body.velocity[0]) > 0 or math.fabs(agent.body.velocity[1]) > 0):
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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def good_16(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(100, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(500, 300, AP_MASS)
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
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		# #helper.snapshot(screen, tick)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		# #helper.snapshot(screen, tick)
		tick+=1
		time-=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep Patient at it's intended velocity
		if (fireball.body.velocity[0] < AGENT_RUNNING):
			imp = AGENT_RUNNING - fireball.body.velocity[0]
			fireball.body.apply_impulse_at_local_point((imp,0))
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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick: ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# +cause, good, patient, low effort
def good_2(space, screen, options, guess=False, impulse=AGENT_WALKING):
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
	count = 250

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and count > 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30, agent.body.position[1]-30)
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1
		time-=1
		count-=1

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
		if(math.fabs(agent.body.velocity[0]) > 0 or math.fabs(agent.body.velocity[1]) > 0):
			impx = agent.body.velocity[0]*-1
			impy = agent.body.velocity[1]*-1
			agent.body.apply_impulse_at_local_point((impx,impy))
			total.append(math.sqrt(impx**2+impy**2))

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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def good_17(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(500, 300, F_MASS)
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
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		# #helper.snapshot(screen, tick)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		# #helper.snapshot(screen, tick)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick: ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# +cause, good, fireball, high effort
def good_3(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	ch1 = space.add_collision_handler(2, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(100, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(300, 300, AP_MASS)
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
	time = 180
	count=200
	flag = True
	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		#helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and count >0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30, agent.body.position[1]-30)
		#helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1
		time-=1
		count-=1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (agent.body.velocity[0] < impulse and time < 120 and time > 40):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		elif(math.fabs(agent.body.velocity[0]) > 0):
			flag = False
			impx = agent.body.velocity[0]*-1
			agent.body.apply_impulse_at_local_point((impx,0))
			total.append(impx)
		if (math.fabs(fireball.body.velocity[0]) < AGENT_WALKING and flag):
			imp = AGENT_WALKING - math.fabs(fireball.body.velocity[0])
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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# +cause, good, patient, high effort
def good_4(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	fireball = agents.fireball(100, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(900, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(300, 300, AP_MASS)
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
	time = 180
	count=200
	flag = True
	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		#helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and count>0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30, agent.body.position[1]-30)
		#helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1
		time-=1
		count-=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (agent.body.velocity[0] < impulse and time < 120 and time > 40):
			imp = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		elif(math.fabs(agent.body.velocity[0]) > 0):
			flag = False
			impx = agent.body.velocity[0]*-1
			agent.body.apply_impulse_at_local_point((impx,0))
			total.append(impx)
		if (math.fabs(patient.body.velocity[0]) < AGENT_WALKING and flag):
			imp = AGENT_WALKING - math.fabs(patient.body.velocity[0])
			patient.body.apply_impulse_at_local_point((-1*imp,0))

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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# -cause, good, fireball, low effort
def good_5(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(100, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(500, 300, AP_MASS)
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
	time = 100
	count=200

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		# #helper.snapshot(screen, tick)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and count>0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1
		time-=1
		count-=1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep Patient at it's intended velocity
		if (fireball.body.velocity[0] < AGENT_WALKING and time > 40):
			imp = AGENT_WALKING - fireball.body.velocity[0]
			fireball.body.apply_impulse_at_local_point((imp,0))
		if((math.fabs(fireball.body.velocity[0]) > 0 or math.fabs(fireball.body.velocity[1]) > 0) and time < 0):
			impx = fireball.body.velocity[0]*-1
			impy = fireball.body.velocity[1]*-1
			fireball.body.apply_impulse_at_local_point((impx,impy))

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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick: ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# -casue, good, patient, low effort
def good_6(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(500, 300, F_MASS)
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
	time = 100
	count=200

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		# #helper.snapshot(screen, tick)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and count>0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1
		time-=1
		count-=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep Patient at it's intended velocity
		if (patient.body.velocity[0] < AGENT_WALKING and time > 40):
			imp = AGENT_WALKING - patient.body.velocity[0]
			patient.body.apply_impulse_at_local_point((imp,0))
		if((math.fabs(patient.body.velocity[0]) > 0 or math.fabs(patient.body.velocity[1]) > 0) and time < 0):
			impx = patient.body.velocity[0]*-1
			impy = patient.body.velocity[1]*-1
			patient.body.apply_impulse_at_local_point((impx,impy))

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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick: ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# -cause, good, fireball, high effort
def good_7(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	ch1 = space.add_collision_handler(2, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(500, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(900, 300, AP_MASS)
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
	time = 60
	count=150

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and count>0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30, agent.body.position[1]-30)
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1
		time-=1
		count-=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(agent.body.velocity[0]) < impulse and 
			time > 0):
			imp = impulse - math.fabs(agent.body.velocity[0])
			agent.body.apply_impulse_at_local_point((-1*imp,0))
			total.append(imp)
		if(math.fabs(agent.body.velocity[0]) > 0 and time < 0):
			impx = agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((-1*impx,0))
			total.append(-1*impx)
		
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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# -cause, good, patient, high effort
def good_8(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	time = 60
	count=150

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and count>0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30, agent.body.position[1]-30)
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1
		time-=1
		count-=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(agent.body.velocity[0]) < impulse and 
			time > 0):
			imp = impulse - math.fabs(agent.body.velocity[0])
			agent.body.apply_impulse_at_local_point((-1*imp,0))
			total.append(imp)
		if(math.fabs(agent.body.velocity[0]) > 0 and time < 0):
			impx = agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((-1*impx,0))
			total.append(-1*impx)

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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# ?cause, good, fireball, low effort
def good_9(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	ch1 = space.add_collision_handler(2, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(300, 200, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(600, 500, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(300, 300, AP_MASS)
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
	time = 70
	count=150

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and count>0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30, agent.body.position[1]-30)
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1
		time-=1
		count-=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		if (math.fabs(fireball.body.velocity[0]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(fireball.body.velocity[0])
			fireball.body.apply_impulse_at_local_point((imp,0))
		
		if (math.fabs(patient.body.velocity[1]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(patient.body.velocity[1])
			patient.body.apply_impulse_at_local_point((0,-1*imp))
		
		if (math.fabs(agent.body.velocity[1]) < impulse and math.fabs(agent.body.velocity[0]) < impulse and
			len(handlers.collision) == 0 and time < 30):
			impy = impulse/3.0 - math.fabs(agent.body.velocity[1])
			impx = impulse - math.fabs(agent.body.velocity[0])
			agent.body.apply_impulse_at_local_point((impx,-1*impy))
			total.append(math.sqrt(impy**2+impx**2))
		elif (len(handlers.collision) > 0):
			impx = agent.body.velocity[0]
			impy = agent.body.velocity[1]
			agent.body.apply_impulse_at_local_point((-1*impx,-1*impy))
			total.append(math.fabs(math.sqrt(impx**2 + impy**2)))
		
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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# ?cause, good, patient, low effort
def good_10(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	fireball = agents.fireball(600, 500, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(300, 200, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(300, 300, AP_MASS)
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
	time = 70
	count=150

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and count>0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30, agent.body.position[1]-30)
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1
		time-=1
		count-=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		if (math.fabs(patient.body.velocity[0]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(patient.body.velocity[0])
			patient.body.apply_impulse_at_local_point((imp,0))
		if (math.fabs(fireball.body.velocity[1]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(fireball.body.velocity[1])
			fireball.body.apply_impulse_at_local_point((0,-1*imp))
		if (math.fabs(agent.body.velocity[1]) < impulse and math.fabs(agent.body.velocity[0]) < impulse and
			len(handlers.collision) == 0 and time < 30):
			impy = impulse/3.0 - math.fabs(agent.body.velocity[1])
			impx = impulse - math.fabs(agent.body.velocity[0])
			agent.body.apply_impulse_at_local_point((impx,-1*impy))
			total.append(math.sqrt(impy**2+impx**2))
		elif (len(handlers.collision) > 0):
			impx = agent.body.velocity[0]
			impy = agent.body.velocity[1]
			agent.body.apply_impulse_at_local_point((-1*impx,-1*impy))
			total.append(math.fabs(math.sqrt(impx**2 + impy**2)))

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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# ?cause, good, fireball, high effort
def good_11(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	ch1 = space.add_collision_handler(2, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(200, 450, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(525, 150, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(100, 450, AP_MASS)
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
	time = 120
	count=200

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		#helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and count>0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30, agent.body.position[1]-30)
		#helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1
		time-=1
		count-=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		if (math.fabs(fireball.body.velocity[0]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(fireball.body.velocity[0])
			fireball.body.apply_impulse_at_local_point((imp,0))
		if (math.fabs(patient.body.velocity[1]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(patient.body.velocity[1])
			patient.body.apply_impulse_at_local_point((0,imp))
		if (math.fabs(agent.body.velocity[0]) < impulse and time > 0):
			imp = impulse - math.fabs(agent.body.velocity[0])
			agent.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		elif(math.fabs(agent.body.velocity[0]) > 0):
			impx = agent.body.velocity[0]*-1
			agent.body.apply_impulse_at_local_point((impx,0))
			total.append(impx)
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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# ?cause, good, patient, high effort
def good_12(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	ch1 = space.add_collision_handler(2, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(525, 150, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(200, 450, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(100, 450, AP_MASS)
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
	time = 120
	count = 200	
	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		#helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and count > 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30, agent.body.position[1]-30)
		#helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1
		time-=1
		count-=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		if (math.fabs(patient.body.velocity[0]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(patient.body.velocity[0])
			patient.body.apply_impulse_at_local_point((imp,0))
		if (math.fabs(fireball.body.velocity[1]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(fireball.body.velocity[1])
			fireball.body.apply_impulse_at_local_point((0,imp))
		if (math.fabs(agent.body.velocity[0]) < impulse and time > 0):
			imp = impulse - math.fabs(agent.body.velocity[0])
			agent.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		elif(math.fabs(agent.body.velocity[0]) > 0):
			impx = agent.body.velocity[0]*-1
			agent.body.apply_impulse_at_local_point((impx,0))
			total.append(impx)
		
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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# +cause, bad, fireball, low effort
def short_distance_fireball(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	ch1 = space.add_collision_handler(2, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2

	# dynamic friction
	space.damping = DYN_FRICTION
	
	# add shapes
	fireball = agents.fireball(800, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(900, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(700, 300, AP_MASS)
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

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		# #helper.snapshot(screen, tick)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

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
			total.append(imp)
		elif (len(handlers.collision) == 1):
			imp = agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((-1*imp,0))
			total.append(math.fabs(imp))

		# append positional values to each list
		xImpsAgent.append(agent.body.position[0])
		yImpsAgent.append(agent.body.position[1])
		xImpsPatient.append(patient.body.position[0])
		yImpsPatient.append(patient.body.position[1])
		xImpsFireball.append(fireball.body.position[0])
		yImpsFireball.append(fireball.body.position[1])

		
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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total)
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# +cause, bad, patient, low effort
def short_distance_patient(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(800, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(700, 300, AP_MASS)
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

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		# #helper.snapshot(screen, tick)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

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
			total.append(imp)
		elif (len(handlers.collision) == 1):
			imp = agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((-1*imp,0))
			total.append(math.fabs(imp))

		# append positional values to each list
		xImpsAgent.append(agent.body.position[0])
		yImpsAgent.append(agent.body.position[1])
		xImpsPatient.append(patient.body.position[0])
		yImpsPatient.append(patient.body.position[1])
		xImpsFireball.append(fireball.body.position[0])
		yImpsFireball.append(fireball.body.position[1])

		
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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total)
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# +cause, bad, fireball high effort
def sim_2_patient(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		# #helper.snapshot(screen, tick)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent	 = (agent.body.position[0]-30,agent.body.position[1]-30)
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

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
			total.append(imp)
		if (math.fabs(patient.body.velocity[0]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(patient.body.velocity[0])
			patient.body.apply_impulse_at_local_point((-1*imp,0))

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
			screen.blit(agentSprite, position_agent	)

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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# +cause, bad, patient, high effort
def sim_2_fireball(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		# #helper.snapshot(screen, tick)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent	 = (agent.body.position[0]-30,agent.body.position[1]-30)
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

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
			total.append(imp)
		if (math.fabs(fireball.body.velocity[0]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(fireball.body.velocity[0])
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
			screen.blit(agentSprite, position_agent	)

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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# -cause, bad, fireball, low effort
def no_touch_fireball(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	ch1 = space.add_collision_handler(2, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2

	# dynamic friction
	space.damping = DYN_FRICTION
	
	# add shapes
	fireball = agents.fireball(100, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(900, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(500, 400, AP_MASS)
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
	time = 160

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		# #helper.snapshot(screen, tick)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent	 = (agent.body.position[0]-30,agent.body.position[1]-30)
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1
		time -= 1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Agent at it's intended velocity for some duration
		if (fireball.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - fireball.body.velocity[0]
			fireball.body.apply_impulse_at_local_point((imp,0))

		# append positional values to each list
		xImpsAgent.append(agent.body.position[0])
		yImpsAgent.append(agent.body.position[1])
		xImpsPatient.append(patient.body.position[0])
		yImpsPatient.append(patient.body.position[1])
		xImpsFireball.append(fireball.body.position[0])
		yImpsFireball.append(fireball.body.position[1])

		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)
			screen.blit(patientSprite, position_patient)
			screen.blit(agentSprite, position_agent	)

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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total)
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# -cause, bad, patient, low effort
def no_touch_patient(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	ch1 = space.add_collision_handler(2, 1)
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
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		# #helper.snapshot(screen, tick)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# set clock
	clock = pygame.time.Clock()

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent	 = (agent.body.position[0]-30,agent.body.position[1]-30)
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
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

		# append positional values to each list
		xImpsAgent.append(agent.body.position[0])
		yImpsAgent.append(agent.body.position[1])
		xImpsPatient.append(patient.body.position[0])
		yImpsPatient.append(patient.body.position[1])
		xImpsFireball.append(fireball.body.position[0])
		yImpsFireball.append(fireball.body.position[1])

		
		# setup display and run sim based on whether it's truth or guess	
		if(not guess):
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			helper.setBackground(screen)
			screen.blit(fireSprite, position_fireball)
			screen.blit(patientSprite, position_patient)
			screen.blit(agentSprite, position_agent	)

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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total)
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# -cause, bad, fireball, high effort
def sim_1_fireball(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		# #helper.snapshot(screen, tick)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent	 = (agent.body.position[0]-30,agent.body.position[1]-30)
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

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
			total.append(imp)
		if (fireball.body.velocity[0] < AGENT_WALKING):
			imp = AGENT_WALKING - fireball.body.velocity[0]
			fireball.body.apply_impulse_at_local_point((imp,0))

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
			screen.blit(agentSprite, position_agent	)

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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# -cause, bad, patient, high effort
def sim_1_patient(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		# #helper.snapshot(screen, tick)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent	 = (agent.body.position[0]-30,agent.body.position[1]-30)
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

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
			total.append(imp)
		if (patient.body.velocity[0] < AGENT_WALKING):
			imp = AGENT_WALKING - patient.body.velocity[0]
			patient.body.apply_impulse_at_local_point((imp,0))

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
			screen.blit(agentSprite, position_agent	)

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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# ?cause, bad, fireball, low effort
def static_fireball(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	ch1 = space.add_collision_handler(2,1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	ch1.post_solve = handlers.rem3
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(300, 360, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(750, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(650, 400, AP_MASS)
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
	count = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		# #helper.snapshot(screen, tick)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent	 = (agent.body.position[0]-30,agent.body.position[1]-30)
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Patient at it's intended velocity for some duration
		if (fireball.body.velocity[0] < impulse and fireball.body.velocity[1] < AGENT_RUNNING and \
				len(handlers.collision) == 0):
			impx = impulse - fireball.body.velocity[0]
			impy = AGENT_WALKING - fireball.body.velocity[1]
			fireball.body.apply_impulse_at_local_point((impx,0))

			# if 	collision between agent and patient, have agent push back once
		if (len(handlers.collision) != 0 and count==0):
			count+=1
			try:
				agent.body.apply_impulse_at_local_point((handlers.totalImpulse[0][0], 
					handlers.totalImpulse[0][1]))
				total.append(math.fabs(handlers.totalImpulse[0][0]) + \
					math.fabs(handlers.totalImpulse[0][1]))
			except:
				pass
		
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
			screen.blit(agentSprite, position_agent	)

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
		handlers.totalImpulse = []
	except:
		print("Exited before collision.")
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print("Total impulse: ", sum(total), "Tick ", tick)
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# ?cause, bad, patient, low effort
def static_patient(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(750, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(300, 360, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(650, 400, AP_MASS)
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
	count = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		# #helper.snapshot(screen, tick)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent	 = (agent.body.position[0]-30,agent.body.position[1]-30)
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
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

			# if 	collision between agent and patient, have agent push back once
		if (len(handlers.collision) != 0 and count==0):
			count+=1
			try:
				agent.body.apply_impulse_at_local_point((handlers.totalImpulse[0][0], 
					handlers.totalImpulse[0][1]))
				total.append(math.fabs(handlers.totalImpulse[0][0]) + \
					math.fabs(handlers.totalImpulse[0][1]))
			except:
				pass
		
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
			screen.blit(agentSprite, position_agent	)

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
		handlers.totalImpulse = []
	except:
		print("Exited before collision.")
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print("Total impulse: ", sum(total), "Tick ", tick)
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# ?cause, bad, fireball, high effort
def bump_fireball(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	ch1 = space.add_collision_handler(2,1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	ch1.post_solve = handlers.rem3
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(200, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(750, 250, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(450, 400, AP_MASS)
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
	count = 0
	time = 111
	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		# #helper.snapshot(screen, tick)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent	 = (agent.body.position[0]-30,agent.body.position[1]-30)
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1
		time-=1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Patient at it's intended velocity for some duration
		if (fireball.body.velocity[0] < AGENT_WALKING and fireball.body.velocity[1] < AGENT_WALKING and
				len(handlers.collision) == 0):
			impx = AGENT_WALKING - fireball.body.velocity[0]
			impy = AGENT_WALKING - fireball.body.velocity[1]
			fireball.body.apply_impulse_at_local_point((impx,0))

		if (time < 0 and agent.body.velocity[0] < impulse and 
				len(handlers.collision) == 0):
			impx = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((impx,0))
			total.append(impx)
		if (time < 0 and math.fabs(agent.body.velocity[1]) < impulse/5.0 and
				len(handlers.collision) == 0):
			impy = impulse/5.0 - agent.body.velocity[1]
			agent.body.apply_impulse_at_local_point((0, -1*impy))
			total.append(impy)
		if(len(handlers.collision) > 0 and math.fabs(agent.body.velocity[0]) > 0 and math.fabs(agent.body.velocity[1]) > 0):
			impx = agent.body.velocity[0]*-1
			impy = agent.body.velocity[1]*-1
			agent.body.apply_impulse_at_local_point((impx,impy))
			total.append(math.sqrt(impx**2+impy**2))
		if (len(handlers.collision) != 0 and count==0):
			count+=1
			try:
				agent.body.apply_impulse_at_local_point((handlers.totalImpulse[0][0], 
					handlers.totalImpulse[0][1]))
				total.append(math.fabs(handlers.totalImpulse[0][0]) + \
					math.fabs(handlers.totalImpulse[0][1]))
			except:
				pass
		
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
			screen.blit(agentSprite, position_agent	)

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
		handlers.totalImpulse = []
	except:
		print("Exited before collision.")
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

# ?cause, bad, patient, high effort
def bump_patient(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(750, 250, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(200, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	agent = agents.agent(450, 400, AP_MASS)
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
	count = 0
	time = 111
	# animation flag and counter
	x = 0
	cnt = 0

	# pause before showing clip
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		# #helper.snapshot(screen, tick)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent	 = (agent.body.position[0]-30,agent.body.position[1]-30)
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1
		time-=1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep the Patient at it's intended velocity for some duration
		if (patient.body.velocity[0] < AGENT_WALKING and patient.body.velocity[1] < AGENT_WALKING and
				len(handlers.collision) == 0):
			impx = AGENT_WALKING - patient.body.velocity[0]
			impy = AGENT_WALKING - patient.body.velocity[1]
			patient.body.apply_impulse_at_local_point((impx,0))

		if (time < 0 and agent.body.velocity[0] < impulse and len(handlers.collision) == 0):
			impx = impulse - agent.body.velocity[0]
			agent.body.apply_impulse_at_local_point((impx,0))
			total.append(impx)
		
		if (time < 0 and math.fabs(agent.body.velocity[1]) < impulse/5.0 and len(handlers.collision) == 0):
			impy = impulse/5.0 - agent.body.velocity[1]
			agent.body.apply_impulse_at_local_point((0, -1*impy))
			total.append(impy)
		
		if(len(handlers.collision) > 0 and math.fabs(agent.body.velocity[0]) > 0 and math.fabs(agent.body.velocity[1]) > 0):
			impx = agent.body.velocity[0]*-1
			impy = agent.body.velocity[1]*-1
			agent.body.apply_impulse_at_local_point((impx,impy))
			total.append(math.sqrt(impx**2+impy**2))
		
		if (len(handlers.collision) != 0 and count==0):
			count+=1
			try:
				agent.body.apply_impulse_at_local_point((handlers.totalImpulse[0][0], 
					handlers.totalImpulse[0][1]))
				total.append(math.fabs(handlers.totalImpulse[0][0]) + \
					math.fabs(handlers.totalImpulse[0][1]))
			except:
				pass
		
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
			screen.blit(agentSprite, position_agent	)

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
		handlers.totalImpulse = []
	except:
		print("Exited before collision.")
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def good_14(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	fireball = agents.fireball(100, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(900, 300, AP_MASS)
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
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		# #helper.snapshot(screen, tick)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		# #helper.snapshot(screen, tick)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1
		time-=1

		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# keep Patient at it's intended velocity
		if (fireball.body.velocity[0] < AGENT_RUNNING and len(handlers.collision) == 0):
			imp = AGENT_RUNNING - fireball.body.velocity[0]
			fireball.body.apply_impulse_at_local_point((imp,0))
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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick: ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)

def good_15(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# Set up space dictionary
	config = {"scene" : pygame.display.get_surface().get_size()[0]}
	config['name'] = sys._getframe().f_code.co_name
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	# helper.wait(screen, space, options, agent, fireball, patient)
	for i in range(25):
		# #helper.snapshot(screen, tick, sys._getframe().f_code.co_name)
		# #helper.snapshot(screen, tick)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
		tick+=1

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		# #helper.snapshot(screen, tick)
		agent_position_dict.append({'x' : agent.body.position[0], 'y' : agent.body.position[1]})
		patient_position_dict.append({'x' : patient.body.position[0], 'y' : patient.body.position[1]})
		fireball_position_dict.append({'x' : fireball.body.position[0], 'y' : fireball.body.position[1]})
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
	# Create dictionary for simulation to be turned into json
	config['ticks'] = tick
	sim_dict['config'] = config
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	sim_dict["objects"] = bodies_dict
	with open(path+sys._getframe().f_code.co_name+".json", "w") as j:
		json.dump(sim_dict, j, indent=2)
	# output to user and return tuple
	print "Total impulse: ", sum(total), "Tick: ", tick
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, 
		xImpsFireball, yImpsFireball)