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


	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1

		# update pymunk space
		space.step(1/50.0)

	point_of_collision = tick
	# print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(100):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		# position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))

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

	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1

		# update pymunk space
		space.step(1/50.0)

	point_of_collision = tick
	# print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(100):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		# position_agent = (agent.body.position[0]-30,agent.body.position[1]-30)
		#helper.snapshot(screen, tick)
		tick+=1
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))

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

		# keep the Patient at it's intended velocity for some duration
		if (patient.body.velocity[0] < impulse and patient.body.velocity[1] < AGENT_RUNNING and \
				len(handlers.collision) == 0):
			impx = impulse - patient.body.velocity[0]
			impy = AGENT_WALKING - patient.body.velocity[1]
			patient.body.apply_impulse_at_local_point((impx,0))

		# update pymunk space
		space.step(1/50.0)	
	
	# Run counterfactual
	for i in range(100):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))
		
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

		# update pymunk space
		space.step(1/50.0)	
	
	point_of_collision = tick
	# print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(100):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))

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

		# update pymunk space
		space.step(1/50.0)	
	
	point_of_collision = tick
	# print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(100):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))

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

		# keep Patient at it's intended velocity
		if (patient.body.velocity[0] < AGENT_RUNNING):
			imp = AGENT_RUNNING - patient.body.velocity[0]
			patient.body.apply_impulse_at_local_point((imp,0))

		# set clock
		clock = pygame.time.Clock()

		# update pymunk space
		space.step(1/50.0)	
	
	point_of_collision = tick
	# print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(150):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))

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

		# update pymunk space
		space.step(1/50.0)	

	# Run counterfactual
	for i in range(150):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))

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

		# update pymunk space
		space.step(1/50.0)	
	
	point_of_collision = tick
	# print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(length_of_counterfactual):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))

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

		# update pymunk space
		space.step(1/50.0)	
	
	# Run counterfactual
	for i in range(length_of_counterfactual):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))

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

		# update pymunk space
		space.step(1/50.0)
	
	# Run counterfactual
	for i in range(length_of_counterfactual):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))

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

	# run simulation
	while running and len(handlers.PF_COLLISION) == 0:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		tick+=1
		time -= 1
		# keep the Agent at it's intended velocity for some duration
		if (patient.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - patient.body.velocity[0]
			patient.body.apply_impulse_at_local_point((imp,0))

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

# # Experiment 1 simulations

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
	pygame.display.set_caption("Simulation 13: Victim Moving, Harm Moving")
	
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 97

	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = AGENT_WALKING
	factual_impulse_fireball = AGENT_WALKING

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

	running = True
	tick = 0
	time = 89

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

		
		# keep the Agent at it's intended velocity for some duration
		if (fireball.body.velocity[0] < AGENT_WALKING):
			imp = AGENT_WALKING - fireball.body.velocity[0]
			fireball.body.apply_impulse_at_local_point((imp,0))
		if (math.fabs(patient.body.velocity[0]) < AGENT_WALKING and len(handlers.collision) == 0):
			imp = AGENT_WALKING - math.fabs(patient.body.velocity[0])
			patient.body.apply_impulse_at_local_point((-1*imp, 0))


		# update pymunk space
		space.step(1/50.0)
	
	# Run counterfactual
	for i in range(length_of_counterfactual):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))


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
	pygame.display.set_caption("Simulation 14: Victim Moving, Harm Static")
	
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 97

	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = AGENT_WALKING
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
	fireball = agents.fireball(450, 200, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(800, 400, AP_MASS)
	space.add(patient.body, patient.shape)

	running = True
	tick = 0
	time = 89

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
		
		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(patient.body.velocity[0]) < AGENT_WALKING and len(handlers.collision) == 0):
			imp = AGENT_WALKING - math.fabs(patient.body.velocity[0])
			patient.body.apply_impulse_at_local_point((-1*imp, 0))

		# update pymunk space
		space.step(1/50.0)
	
	point_of_collision = tick
	# print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(length_of_counterfactual):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))
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
	pygame.display.set_caption("Simulation 15: Victim Static, Harm Moving")
	
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 48

	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = 0
	factual_impulse_fireball = AGENT_RUNNING

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
	fireball = agents.fireball(800, 200, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(350, 400, AP_MASS)
	space.add(patient.body, patient.shape)

	running = True
	tick = 0
	time = 40

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
		
		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(fireball.body.velocity[0]) < AGENT_RUNNING):# and len(handlers.collision) == 0):
			imp = AGENT_RUNNING - math.fabs(fireball.body.velocity[0])
			fireball.body.apply_impulse_at_local_point((-1*imp, 0))

		# update pymunk space
		space.step(1/50.0)
	
	point_of_collision = tick
	# print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(length_of_counterfactual):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))

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

def victim_static_static(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Agent rests on left side of screen. Fireball rests on right side of screen.
	Patient rests in between Agent and Fireball. 
	Agent pushes resting Patient into resting Fireball.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 16: Victim Static, Harm Static")
	
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 42

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
	fireball = agents.fireball(800, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(500, 300, AP_MASS)
	space.add(patient.body, patient.shape)

	running = True
	tick = 0
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

		# update pymunk space
		space.step(1/50.0)
	
	point_of_collision = tick
	# print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(length_of_counterfactual):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))

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
	pygame.display.set_caption("Simulation 19: Harm Static, Victim Moving")
	
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 48

	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = AGENT_RUNNING
	factual_impulse_fireball = 0

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
	running = True
	tick = 0
	time = 40

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
		
		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(patient.body.velocity[0]) < AGENT_RUNNING):# and len(handlers.collision) == 0):
			imp = AGENT_RUNNING - math.fabs(patient.body.velocity[0])
			patient.body.apply_impulse_at_local_point((-1*imp, 0))

		# update pymunk space
		space.step(1/50.0)
	
	point_of_collision = tick
	# print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(length_of_counterfactual):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))

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

def harm_static_static(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	'''
	Agent rests on left side of screen. Patient rests on right side of screen.
	Fireball rests in between Agent and Patient. 
	Agent pushes resting Fireball into resting Patient.

	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 20: Harm Static, Victim Static")
	
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 42

	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = 0
	factual_impulse_fireball = 0

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

	running = True
	tick = 0
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

		# update pymunk space
		space.step(1/50.0)
	
	point_of_collision = tick
	# print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(length_of_counterfactual):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))

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
	pygame.display.set_caption("Simulation 18: Harm Moving, Victim Static")
	
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 97

	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = 0
	factual_impulse_fireball = AGENT_WALKING

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
	
	running = True
	tick = 0
	time = 89

	# animation flag and counter
	x = 0
	cnt = 0

	# set cloc
	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		tick+=1
		time -= 1

		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(fireball.body.velocity[0]) < AGENT_WALKING and len(handlers.collision) == 0):
			imp = AGENT_WALKING - math.fabs(fireball.body.velocity[0])
			fireball.body.apply_impulse_at_local_point((-1*imp, 0))
		
		# update pymunk space
		space.step(1/50.0)
	
	point_of_collision = tick
	# print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(length_of_counterfactual):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))

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
	pygame.display.set_caption("Simulation 17: Harm Moving, Victim Moving")
	
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 97

	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = AGENT_WALKING
	factual_impulse_fireball = AGENT_WALKING

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
	patient = agents.patient(100, 200, AP_MASS)
	space.add(patient.body, patient.shape)

	running = True
	tick = 0
	time = 89

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
		
		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(fireball.body.velocity[0]) < AGENT_WALKING and len(handlers.collision) == 0):
			imp = AGENT_WALKING - math.fabs(fireball.body.velocity[0])
			fireball.body.apply_impulse_at_local_point((-1*imp,0))
		if (patient.body.velocity[0] < AGENT_WALKING):
			imp = AGENT_WALKING - patient.body.velocity[0]
			patient.body.apply_impulse_at_local_point((imp, 0))

		# update pymunk space
		space.step(1/50.0)
	
	point_of_collision = tick
	# print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(length_of_counterfactual):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))

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

# Dynamics simulations

def sim_1_patient(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 84

	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = AGENT_WALKING
	factual_impulse_fireball = 0

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

	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		tick+=1

		# keep the Agent at it's intended velocity for some duration
		if (patient.body.velocity[0] < AGENT_WALKING):
			imp = AGENT_WALKING - patient.body.velocity[0]
			patient.body.apply_impulse_at_local_point((imp,0))


		# update pymunk space
		space.step(1/50.0)	
	
	point_of_collision = tick
	# print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(length_of_counterfactual):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))

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

def sim_1_fireball(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 84

	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = 0
	factual_impulse_fireball = AGENT_WALKING

	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"] = screen
	ch0.post_solve = handlers.rem0
	ch1 = space.add_collision_handler(2, 1)
	ch1.data["surface"] = screen
	ch1.begin = handlers.rem2
	space.damping = DYN_FRICTION

	# add shapes
	fireball = agents.fireball(400, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(900, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		tick+=1


		# keep the Agent at it's intended velocity for some duration
		if (fireball.body.velocity[0] < AGENT_WALKING):
			imp = AGENT_WALKING - fireball.body.velocity[0]
			fireball.body.apply_impulse_at_local_point((imp,0))

		# update pymunk space
		space.step(1/50.0)	
	
	point_of_collision = tick
	# print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(length_of_counterfactual):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))

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

def sim_2_patient(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 39

	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = AGENT_WALKING
	factual_impulse_fireball = 0

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
	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		tick+=1

		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(patient.body.velocity[0]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(patient.body.velocity[0])
			patient.body.apply_impulse_at_local_point((-1*imp,0))

		# update pymunk space
		space.step(1/50.0)	
	
	point_of_collision = tick
	# print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(length_of_counterfactual):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))

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

def sim_2_fireball(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# Simulation tick at which Agent factually collides with Patient
	point_of_collision = 39

	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = 0
	factual_impulse_fireball = AGENT_WALKING

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
	running = True
	tick = 0

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		tick+=1

		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(fireball.body.velocity[0]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(fireball.body.velocity[0])
			fireball.body.apply_impulse_at_local_point((-1*imp,0))


		# update pymunk space
		space.step(1/50.0)	
	point_of_collision = tick
	# print "Point of collision occurs at tick {0}".format(point_of_collision)
	
	# Run counterfactual
	for i in range(length_of_counterfactual):
		# update fireball sprite according to ball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)
		tick+=1
		
		# Apply noise to the velocity of the Patient and Fireball
		if (patient.body.velocity[0] < factual_impulse_patient or patient.body.velocity[1] < factual_impulse_patient):
			# Sample x and y velocity from normal distribution and apply
			patient.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_patient*helper.sample_trajectory()))
		if (fireball.body.velocity[0] < factual_impulse_fireball or fireball.body.velocity[1] < factual_impulse_fireball):
			# Sample x and y velocity from normal distribution and apply
			fireball.body.apply_impulse_at_local_point((factual_impulse_patient*helper.sample_trajectory(),
				factual_impulse_fireball*helper.sample_trajectory()))

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