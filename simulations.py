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
	ch0.data["surface"]=screen
	ch0.post_solve=handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"]=screen
	ch1.begin=handlers.rem2
	space.damping = 0.2
	
	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	cone = agents.patient(400, 300)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(250, 300)
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
	tick=0
	while running and tick<95:
		tick+=1
		
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		
		# Check if the velocity is less than it's 'max' velocity. If so,
		# apply an impulse to the agent and add that impulse value to total
		if (cylinder.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((2*imp,0))
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
	
	# handlers.remove value from collision list and print out resulting effort
	try:
		handlers.collision = []
	except:
		print("Exited before collision.")
	#print("Total impulse: ", sum(total))
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, xImpsFireball, yImpsFireball)

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
	space.damping = 0.2
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
	while running and tick<115:
		tick += 1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		'''
		Check if the velocity is less than it's 'max' velocity. If so,
		apply an impulse to the agent and add that impulse value to total
		'''
		if (cylinder.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((2*imp,0))
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

	# handlers.remove value from collision list and print out resulting effort
	try:
		handlers.collision = []
	except:
		print("Exited before collision.")
	print("Total impulse: ", sum(total), "Tick ", tick)
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, xImpsFireball, yImpsFireball)

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
	ch0.data["surface"]=screen
	ch0.post_solve=handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"]=screen
	ch1.begin=handlers.rem2
	space.damping = 0.2
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
	total=[]
	running = True
	tick = 0
	while running and tick < 133:
		tick+=1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		'''
		Check if the velocity is less than it's 'max' velocity. If so,
		apply an impulse to the agent and add that impulse value to total
		'''
		if (cylinder.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((2*imp,0))
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

	# handlers.remove value from collision list and print out resulting effort
	try:
		handlers.collision = []
	except:
		print("Exited before collision.")
	print("Total impulse: ", sum(total), "Tick ", tick)
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, xImpsFireball, yImpsFireball)

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
	ch0=space.add_collision_handler(0,2)
	ch0.data["surface"]=screen
	ch0.post_solve=handlers.rem0
	ch1=space.add_collision_handler(0,1)
	ch1.data["surface"]=screen
	ch1.begin=handlers.rem2
	ch1.post_solve=handlers.rem3
	space.damping=0.2

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
	total=[]
	running = True
	tick = 0
	count = 0
	while running and tick < 140:
		tick+=1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		# Check if the velocity is less than it's 'max' velocity.
		if (cone.body.velocity[0] < impulse and cone.body.velocity[1] < 180 and \
				len(handlers.collision) == 0):
			impx = impulse - cone.body.velocity[0]
			impy = 180 - cone.body.velocity[1]
			cone.body.apply_impulse_at_local_point((impx,impy))

		# if there is a collision between agent and patient, have agent push back once
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

	# handlers.remove value from collision list and print out resulting effort
	try:
		handlers.collision = []
		handlers.totalImpulse = []
	except:
		print("Exited before collision.")
	print("Total impulse: ", sum(total), "Tick ", tick)
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, xImpsFireball, yImpsFireball)

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
	ch0=space.add_collision_handler(0,2)
	ch0.data["surface"]=screen
	ch0.post_solve=handlers.rem0
	ch1=space.add_collision_handler(0,1)
	ch1.data["surface"]=screen
	#ch1.post_solve=handlers.rem1
	ch1.begin=handlers.rem2
	space.damping=0.2

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
	while running and tick<149:
		tick+=1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		if (cone.body.velocity[0] < 200 and len(handlers.collision) == 0):
			imp = 150 - cone.body.velocity[0]
			cone.body.apply_impulse_at_local_point((imp,0))
		if (cylinder.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = 450 - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((imp,0))
			total.append(imp)
		if (len(handlers.collision) == 1 and count == 0):
			count+=1
			cone.body.apply_impulse_at_local_point((-50,0))
		if (len(handlers.collision) != 0 and cylinder.body.velocity[0] > 0):
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
	# handlers.remove value from collision list and print out resulting effort
	try:
		handlers.collision = []
		handlers.totalImpulse = []
	except:
		print("Exited before collision.")
	print("Total impulse: ", sum(total), "Tick: ", tick)
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, xImpsFireball, yImpsFireball)

def fastCollision(space, screen, options, guess=False, impulse=270):
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
	ch0=space.add_collision_handler(0,2)
	ch0.data["surface"]=screen
	ch0.post_solve=handlers.rem0
	ch1=space.add_collision_handler(0,1)
	ch1.data["surface"]=screen
	ch1.begin=handlers.rem2
	space.damping=0.2
	
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
	while running and tick<154:
		tick+=1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

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

	# handlers.remove value from collision list and print out resulting effort
	try:
		handlers.collision = []
	except:
		print("Exited before collision.")
	print("Total impulse: ", sum(total), "Tick: ", tick)
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, xImpsFireball, yImpsFireball)

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
	ch0=space.add_collision_handler(0,2)
	ch0.data["surface"]=screen
	ch0.post_solve=handlers.rem0
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
	total=[]
	running = True
	tick = 0
	time=80
	while running and tick<186:
		tick+=1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		time-=1
		if (cone.body.velocity[0] < 100):
			imp = 100 - cone.body.velocity[0]
			cone.body.apply_impulse_at_local_point((imp,0))
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

	print("Total impulse: ", sum(total), "Tick: ", tick)
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, xImpsFireball, yImpsFireball)

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
	ch0=space.add_collision_handler(0,2)
	ch0.data["surface"]=screen
	ch0.post_solve=handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"]=screen
	ch1.begin = handlers.rem2
	space.damping = 0.2

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
	total=[]
	running = True
	tick = 0
	time=50
	while running and tick<137:
		tick+=1
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		time -=1
		'''
		Check if the velocity is less than it's 'max' velocity. If so,
		apply an impulse to the agent and add that impulse value to total
		'''
		if (cylinder.body.velocity[0] < impulse and len(handlers.collision) == 0):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((2*imp,0))
			total.append(imp)
		elif (time == 10):
			imp = impulse - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((2*imp,0))
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
		print("Exited before collision.")
	print("Total impulse: ", sum(total), "Tick: ", tick)
	return (xImpsAgent, yImpsAgent, xImpsPatient, yImpsPatient, xImpsFireball, yImpsFireball)

def mediumPush(space, screen, options):
	'''
	Simulation of Cylinder pushing Cone into Fireball over a medium distance
	before letting go.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 11: Medium Push Cylinder")
	# set up collision handlers
	ch0=space.add_collision_handler(0,2)
	ch0.data["surface"]=screen
	ch0.post_solve=handlers.rem0
	space.damping = 0.2

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	cone = agents.patient(200, 300)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(150, 300)
	space.add(cylinder.body, cylinder.shape)

	time = 70
	total = []
	running = True
	while running:
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		time -= 1
		'''
		Check if the velocity is less than it's 'max' velocity. If so,
		apply an impulse to the agent and add that impulse value to total
		'''
		if (cylinder.body.velocity[0] < 150 and time > 0):
			imp = 150.0 - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((2*imp,0))
			total.append(math.fabs(imp))
		if (time == 0):
			cylinder.body.apply_impulse_at_local_point((-1*cylinder.body.velocity[0],0))
		
		# set clock
		clock = pygame.time.Clock()
		# setup display and run sim
		screen.fill((255,255,255))
		space.step(1/50.0)
		space.debug_draw(options)
		pygame.display.flip()
		clock.tick(50)

	# print out resulting effort
	print("Total impulse: ", sum(total))
	return

def longPush(space, screen, options):
	'''
	Simulation of Cylinder pushing Cone into Fireball over complete
	distance.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 12: Long Push Cylinder")
	# set up collision handlers
	ch0=space.add_collision_handler(0,2)
	ch0.data["surface"]=screen
	ch0.post_solve=handlers.rem0
	ch0.begin=handlers.rem2
	space.damping = 0.2

	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)	
	cone = agents.patient(200, 300)
	space.add(cone.body, cone.shape)	
	cylinder = agents.agent(150, 300)
	#cylinder.shape.elasticity = 0
	space.add(cylinder.body, cylinder.shape)

	total = []
	running = True
	while running:
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
		'''
		Check if the velocity is less than it's 'max' velocity. If so,
		apply an impulse to the agent and add that impulse value to total
		'''
		if (cylinder.body.velocity[0] < 100 and len(handlers.collision) == 0):
			imp = 100.0 - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((2*imp,0))
			total.append(imp)

		# set clock
		clock = pygame.time.Clock()
		# setup display and run sim
		screen.fill((255,255,255))
		space.step(1/50.0)
		space.debug_draw(options)
		pygame.display.flip()
		clock.tick(50)

	# handlers.remove value from collision list and print out resulting effort
	try:
		handlers.collision = []
	except:
		print("Exited before collision.")
	print("Total impulse: ", sum(total))
	return

def touch(space, screen, options):
	'''
	Simulation of Cylinder touching Cone or tapping Cone into Fireball.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 13: Touch Cylinder")
	# set up collision handlers
	ch0=space.add_collision_handler(0,2)
	ch0.data["surface"]=screen
	ch0.post_solve=handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"]=screen
	ch1.begin = handlers.rem2

	space.damping = 0.2
	# add shapes
	ball = agents.fireball(500, 300)
	space.add(ball.body, ball.shape)
	cone = agents.patient(200, 300)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(170, 300)
	space.add(cylinder.body, cylinder.shape)

	total = []
	running = True
	while running:
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		'''
		Check if the velocity is less than it's 'max' velocity. If so,
		apply an impulse to the agent and add that impulse value to total
		'''
		if (cylinder.body.velocity[0] < 250 and len(handlers.collision) == 0):
			imp = 250.0 - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((2*imp,0))
			total.append(imp)

		# set clock
		clock = pygame.time.Clock()
		# setup display and run sim
		screen.fill((255,255,255))
		space.step(1/50.0)
		space.debug_draw(options)
		pygame.display.flip()
		clock.tick(50)

	# handlers.remove value from collision list and print out resulting effort
	try:
		handlers.collision = []
	except:
		print("Exited before collision.")
	print("Total impulse: ", sum(total))
	return

def pushFireball(space, screen, options):
	'''
	Simulation of Cylinder pushing Fireball into Cone.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 14: Push Fireball")
	# set up collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"]=screen
	ch0.post_solve=handlers.rem0
	ch1 = space.add_collision_handler(1, 2)
	ch1.data["surface"]=screen
	ch1.begin=handlers.rem2
	space.damping = 0.2
	# add shapes
	ball = agents.fireball(400, 300)
	space.add(ball.body, ball.shape)
	cone = agents.patient(500, 300)
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(100, 300)
	space.add(cylinder.body, cylinder.shape)
	
	total=[]
	running = True
	while running:
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		'''
		Check if the velocity is less than it's 'max' velocity. If so,
		apply an impulse to the agent and add that impulse value to total
		'''
		if (cylinder.body.velocity[0] < 275 and len(handlers.collision) == 0):
			imp = 275.0 - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((2*imp,0))
			total.append(imp)
		elif (len(handlers.collision) != 0 and cylinder.body.velocity[0] != 0):
			cylinder.body.apply_impulse_at_local_point((-1*cylinder.body.velocity[0],0))
			total.append(math.fabs(imp))

		# set clock
		clock = pygame.time.Clock()
		# setup display and run sim
		screen.fill((255,255,255))
		space.step(1/50.0)
		space.debug_draw(options)
		pygame.display.flip()
		clock.tick(50)

	# handlers.remove value from collision list and print out resulting effort
	try:
		handlers.collision = []
	except:
		print("Exited before collision.")
	print("Total impulse: ", sum(total))
	return

def test(space, screen, options):
	'''
	Current sim for testing extraction of effort from agent.
	space -- pymunk simulation space
	screen -- pygame display Surface
	options -- draw options for pymunk space
	'''
	pygame.display.set_caption("Simulation 14: Test Simulation for Effort Extraction")
	# set up post_solve and begin collision handlers
	ch0 = space.add_collision_handler(0, 2)
	ch0.data["surface"]=screen
	ch0.post_solve=handlers.rem0
	ch1 = space.add_collision_handler(0, 1)
	ch1.data["surface"]=screen
	ch1.begin = handlers.rem2

	# set space damping
	space.damping = 0.2

	# add shapes with necesarry impulses
	ball = agents.fireball(500, 300) # fireball
	space.add(ball.body, ball.shape)	
	cone = agents.patient(400, 300) # patient
	space.add(cone.body, cone.shape)
	cylinder = agents.agent(175, 300) # agent
	space.add(cylinder.body, cylinder.shape)

	'''
	Initialize list of effort variables with first supplied impulse of 150.
	We will add the supplied impulses to this list and sum over it for our 
	final quantity of effort (so far).
	'''
	total = []
	running = True
	while running:
		#allow user to exit
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		'''
		Check if the velocity is less than it's 'max' velocity. If so,
		apply an impulse to the agent and add that impulse value to total
		'''
		if (cylinder.body.velocity[0] < 150 and len(handlers.collision) == 0):
			imp = 150.0 - cylinder.body.velocity[0]
			cylinder.body.apply_impulse_at_local_point((2*imp,0))
			total.append(imp)

		# set clock
		clock = pygame.time.Clock()

		# setup display and run sim
		screen.fill((255,255,255))
		space.step(1/50.0)
		space.debug_draw(options)
		pygame.display.flip()
		clock.tick(50)

	# handlers.remove value from collision list and print out resulting effort
	try:
		handlers.collision = []
	except:
		print("Exited before collision.")
	print("Total impulse: ", sum(total))
	return