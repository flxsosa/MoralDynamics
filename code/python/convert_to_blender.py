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

def long_distance_v1(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Agent pushes Patient into Fireball from a long distance away.
	
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	
	# Set up space dictionary
	space_dict = {"field" : pygame.display.get_surface().get_size()}
	bodies_dict = {}
	agent_position_dict = []
	patient_position_dict = []
	fireball_position_dict = []

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
	helper.wait(screen, space, options, agent, fireball, patient)
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
	
	bodies_dict["agent"] = agent_position_dict
	bodies_dict["patient"] = patient_position_dict
	bodies_dict["fireball"] = fireball_position_dict
	space_dict["objects"] = bodies_dict
	
	with open("j.json", "w") as j:
		json.dump(space_dict, j, indent=2)
	
	# remove value from collision list
	try:
		handlers.collision = []
		handlers.PF_COLLISION = []
	except:
		print "Exited before collision."