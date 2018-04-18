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
length_of_counterfactual = 200

# +cause, good, fireball, low effort
def good_1(space, screen, options, guess=False, impulse=AGENT_WALKING):
	point_of_collision = 184
	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = 0
	factual_impulse_fireball = impulse

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
	running = True
	tick = 0
	time = 40
	count = 250

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick < point_of_collision:#count > 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		tick+=1
		time-=1

		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(fireball.body.velocity[0]) < impulse and 
			len(handlers.collision) == 0):
			imp = impulse - math.fabs(fireball.body.velocity[0])
			fireball.body.apply_impulse_at_local_point((imp,0))

		# update pymunk space
		space.step(1/50.0)	
	
	# Run counterfactual
	for i in range(100):
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

# +cause, good, patient, low effort
def good_2(space, screen, options, guess=False, impulse=AGENT_WALKING):
	point_of_collision = 184
	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = impulse
	factual_impulse_fireball = 0

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
	running = True
	tick = 0
	time = 40
	count = 250

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick < point_of_collision:#count > 0:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		tick+=1
		time-=1

		# keep the Agent at it's intended velocity for some duration
		if (math.fabs(patient.body.velocity[0]) < impulse and 
			len(handlers.collision) == 0):
			imp = impulse - math.fabs(patient.body.velocity[0])
			patient.body.apply_impulse_at_local_point((imp,0))

		# update pymunk space
		space.step(1/50.0)	
	
	# Run counterfactual
	for i in range(100):
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

# +cause, good, fireball, high effort
def good_3(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	point_of_collision = 102

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
	fireball = agents.fireball(900, 300, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(100, 300, AP_MASS)
	space.add(patient.body, patient.shape)

	running = True
	tick = 0
	time = 180
	count=200
	flag = True
	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		tick+=1
		time-=1
		count-=1

		if (math.fabs(fireball.body.velocity[0]) < AGENT_WALKING and flag):
			imp = AGENT_WALKING - math.fabs(fireball.body.velocity[0])
			fireball.body.apply_impulse_at_local_point((-1*imp,0))

		# update pymunk space
		space.step(1/50.0)	

	# Run counterfactual
	for i in range(100):
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

# +cause, good, patient, high effort
def good_4(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	point_of_collision = 102

	factual_impulse_patient = AGENT_WALKING
	factual_impulse_fireball = 0

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

	running = True
	tick = 0
	time = 180
	count=200
	flag = True
	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		tick+=1
		time-=1
		count-=1

		if (math.fabs(patient.body.velocity[0]) < AGENT_WALKING and flag):
			imp = AGENT_WALKING - math.fabs(patient.body.velocity[0])
			patient.body.apply_impulse_at_local_point((-1*imp,0))

		# update pymunk space
		space.step(1/50.0)	

	# Run counterfactual
	for i in range(100):
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

# -cause, good, fireball, low effort
def good_5(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	point_of_collision = 68

	factual_impulse_patient = 0
	factual_impulse_fireball = AGENT_WALKING

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
	running = True
	tick = 0
	time = 100
	count=200

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick<point_of_collision:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)

		tick+=1
		time-=1
		count-=1

		# keep Patient at it's intended velocity
		if (fireball.body.velocity[0] < AGENT_WALKING and time > 40):
			imp = AGENT_WALKING - fireball.body.velocity[0]
			fireball.body.apply_impulse_at_local_point((imp,0))
		if((math.fabs(fireball.body.velocity[0]) > 0 or math.fabs(fireball.body.velocity[1]) > 0) and time < 0):
			impx = fireball.body.velocity[0]*-1
			impy = fireball.body.velocity[1]*-1
			fireball.body.apply_impulse_at_local_point((impx,impy))

		# update pymunk space
		space.step(1/50.0)	
		
	# Run counterfactual
	for i in range(100):
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

# -casue, good, patient, low effort
def good_6(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	point_of_collision = 68

	factual_impulse_patient = AGENT_WALKING
	factual_impulse_fireball = 0

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
	running = True
	tick = 0
	time = 66
	count=200

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick<point_of_collision:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)

		tick+=1
		time-=1
		count-=1

		# keep Patient at it's intended velocity
		if (patient.body.velocity[0] < AGENT_WALKING and time > 40):
			imp = AGENT_WALKING - patient.body.velocity[0]
			patient.body.apply_impulse_at_local_point((imp,0))
		if((math.fabs(patient.body.velocity[0]) > 0 or math.fabs(patient.body.velocity[1]) > 0) and time < 0):
			impx = patient.body.velocity[0]*-1
			impy = patient.body.velocity[1]*-1
			fireball.body.apply_impulse_at_local_point((impx,impy))

		# update pymunk space
		space.step(1/50.0)	
		
	# Run counterfactual
	for i in range(100):
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

# -cause, good, fireball, high effort
def good_7(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	point_of_collision=26

	factual_impulse_patient = 0
	factual_impulse_fireball = 0
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
	time = 60
	count=150

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		tick+=1
		time-=1
		count-=1

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
	
	if (len(handlers.PF_COLLISION) == 0):
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

# -cause, good, patient, high effort
def good_8(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	point_of_collision=26

	factual_impulse_patient = 0
	factual_impulse_fireball = 0
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
	patient = agents.patient(500, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	
	running = True
	tick = 0
	time = 60
	count=150

	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		tick+=1
		time-=1
		count-=1

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
	
	if (len(handlers.PF_COLLISION) == 0):
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

# ?cause, good, fireball, low effort
def good_9(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# Set up space dictionary
	point_of_collision=71

	factual_impulse_patient = AGENT_WALKING
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
	fireball = agents.fireball(300, 200, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(600, 500, AP_MASS)
	space.add(patient.body, patient.shape)
	running = True
	tick = 0
	time = 70
	count=150

	# animation flag and counter
	x = 0
	cnt = 0


	# run simulation
	while running and tick<point_of_collision:	
		tick+=1
		time-=1
		count-=1

		if (math.fabs(fireball.body.velocity[0]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(fireball.body.velocity[0])
			fireball.body.apply_impulse_at_local_point((imp,0))
		
		if (math.fabs(patient.body.velocity[1]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(patient.body.velocity[1])
			patient.body.apply_impulse_at_local_point((0,-1*imp))


		# update pymunk space
		space.step(1/50.0)	
		# Run counterfactual
	for i in range(length_of_counterfactual):
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

# ?cause, good, patient, low effort
def good_10(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	# Set up space dictionary
	point_of_collision=71

	factual_impulse_patient = AGENT_WALKING
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
	fireball = agents.fireball(300, 200, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(600, 500, AP_MASS)
	space.add(patient.body, patient.shape)
	running = True
	tick = 0
	time = 70
	count=150

	# animation flag and counter
	x = 0
	cnt = 0


	# run simulation
	while running and tick<point_of_collision:	
		tick+=1
		time-=1
		count-=1

		if (math.fabs(fireball.body.velocity[0]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(fireball.body.velocity[0])
			fireball.body.apply_impulse_at_local_point((imp,0))
		
		if (math.fabs(patient.body.velocity[1]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(patient.body.velocity[1])
			patient.body.apply_impulse_at_local_point((0,-1*imp))


		# update pymunk space
		space.step(1/50.0)	
		# Run counterfactual
	for i in range(length_of_counterfactual):
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

# ?cause, good, fireball, high effort
def good_11(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	point_of_collision=17
	factual_impulse_patient = AGENT_WALKING
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
	fireball = agents.fireball(525, 150, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(200, 450, AP_MASS)
	space.add(patient.body, patient.shape)

	# lists for impulse values at each timestep, total impulses, runnign flag, and ticks
	running = True
	tick = 0
	time = 120
	count = 200	
	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		tick+=1
		time-=1
		count-=1

		if (math.fabs(patient.body.velocity[0]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(patient.body.velocity[0])
			patient.body.apply_impulse_at_local_point((imp,0))
		if (math.fabs(fireball.body.velocity[1]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(fireball.body.velocity[1])
			fireball.body.apply_impulse_at_local_point((0,imp))

		space.step(1/50.0)	

	# Run counterfactual
	for i in range(length_of_counterfactual):
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

# ?cause, good, patient, high effort
def good_12(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	point_of_collision=17
	factual_impulse_patient = AGENT_WALKING
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
	fireball = agents.fireball(525, 150, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(200, 450, AP_MASS)
	space.add(patient.body, patient.shape)

	# lists for impulse values at each timestep, total impulses, runnign flag, and ticks
	running = True
	tick = 0
	time = 120
	count = 200	
	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick < point_of_collision:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30, fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30, patient.body.position[1]-30)
		tick+=1
		time-=1
		count-=1

		if (math.fabs(patient.body.velocity[0]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(patient.body.velocity[0])
			patient.body.apply_impulse_at_local_point((imp,0))
		if (math.fabs(fireball.body.velocity[1]) < AGENT_WALKING):
			imp = AGENT_WALKING - math.fabs(fireball.body.velocity[1])
			fireball.body.apply_impulse_at_local_point((0,imp))

		space.step(1/50.0)	

	# Run counterfactual
	for i in range(length_of_counterfactual):
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

# +cause, bad, fireball, low effort
def short_distance_fireball(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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

		# update pymunk space
		space.step(1/50.0)
	
	# Run counterfactual
	for i in range(length_of_counterfactual):
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

# +cause, bad, patient, low effort
def short_distance_patient(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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

		# update pymunk space
		space.step(1/50.0)
	
	# Run counterfactual
	for i in range(length_of_counterfactual):
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

# -cause, bad, fireball, low effort
def no_touch_fireball(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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

		# keep the Agent at it's intended velocity for some duration
		if (patient.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - patient.body.velocity[0]
			patient.body.apply_impulse_at_local_point((imp,0))

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

# -cause, bad, patient, low effort
def no_touch_patient(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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

		# keep the Agent at it's intended velocity for some duration
		if (patient.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - patient.body.velocity[0]
			patient.body.apply_impulse_at_local_point((imp,0))


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

		# set clock
		clock = pygame.time.Clock()

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

# ?cause, bad, fireball, low effort
def static_fireball(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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

# ?cause, bad, patient, low effort
def static_patient(space, screen, options, guess=False, impulse=AGENT_RUNNING):
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

		# set clock
		clock = pygame.time.Clock()

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

# ?cause, bad, fireball, high effort
def bump_fireball(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	point_of_collision=130
	
	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = AGENT_WALKING
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
	fireball = agents.fireball(750, 250, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(200, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	running = True
	tick = 0
	count = 0
	time = 111
	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick<point_of_collision:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)

		tick+=1
		time-=1

		# keep the Patient at it's intended velocity for some duration
		if (patient.body.velocity[0] < AGENT_WALKING and patient.body.velocity[1] < AGENT_WALKING and
				len(handlers.collision) == 0):
			impx = AGENT_WALKING - patient.body.velocity[0]
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

# ?cause, bad, patient, high effort
def bump_patient(space, screen, options, guess=False, impulse=AGENT_RUNNING):
	point_of_collision=130
	
	# Parameters of Patient and Fireball in factual simulation
	factual_impulse_patient = AGENT_WALKING
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
	fireball = agents.fireball(750, 250, F_MASS)
	space.add(fireball.body, fireball.shape)
	patient = agents.patient(200, 300, AP_MASS)
	space.add(patient.body, patient.shape)
	running = True
	tick = 0
	count = 0
	time = 111
	# animation flag and counter
	x = 0
	cnt = 0

	# run simulation
	while running and tick<point_of_collision:
		# update fireball sprite according to fireball's position
		position_fireball = (fireball.body.position[0]-30,fireball.body.position[1]-30)
		position_patient = (patient.body.position[0]-30,patient.body.position[1]-30)

		tick+=1
		time-=1

		# keep the Patient at it's intended velocity for some duration
		if (patient.body.velocity[0] < AGENT_WALKING and patient.body.velocity[1] < AGENT_WALKING and
				len(handlers.collision) == 0):
			impx = AGENT_WALKING - patient.body.velocity[0]
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