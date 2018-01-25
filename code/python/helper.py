'''
Set of helper functions for Moral Dynamics 
modules

Felix Sosa
June 27, 2017
'''
import pygame
import numpy as np
#import main

# Sprites used in simulations
BACKGROUND_S = pygame.image.load("Sprites/sand.jpg")
BACKGROUND_G = pygame.image.load("Sprites/grass.jpg")
fireSprite = pygame.image.load("Sprites/firea.png")
patientSprite = pygame.image.load("Sprites/Patient.png")
agentSprite = pygame.image.load("Sprites/Agent.png")

def printHeader():
	'''
	Prints main menu header
	'''
	print("=================================================")
	print("1. Show Simulations")
	print("2. Show Counterfactuals")
	print("0. EXIT")
	print("=================================================")
	print("Please choose an option or [0] to exit:")
	
def printOptions():
	'''
	Prints simulation menu options to user.
	'''
	print("=================================================")
	print("-----AVAILABLE EXPERIMENT 1 SIMS-----")
	print("1. Short Distance v1")
	print("2. Medium Distance v2")
	print("3. Long Distance v1")
	#print("4. Long Distance v2")
	print("4. Static")
	print("5. Slow Collision")
	print("6. Fast Collision")
	print("7. Dodge")
	print("8. Double Push")
	print("9. Medium Push")
	print("1. Long Push")
	print("11. Moving")
	print("12. No Touch")
	print("-----AVAILABLE EXPERIMENT 2 SIMS-----")
	print("13. Victim Moving Moving")
	print("14. Victim Moving Static")
	print("15. Victim Static Moving")
	print("16. Victim Static Static")
	print("17. Harm Moving Moving")
	print("18. Harm Moving Static")
	print("19. Harm Static Moving")
	print("20. Harm Static Static")
	print("-----EXTRA MORAL DYNAMICS SIMS-------")
	print("21. Sim 1 Patient")
	print("22. Sim 1 Fireball")
	print("23. Sim 2 Patient")
	print("24. Sim 2 Fireball")
	print("25. Sim 3 Patient")
	print("26. Sim 3 Fireball")
	print("27. Sim 4 Patient")
	print("28. Sim 4 Fireball")
	print("-----MTURK INTRO SIMS----------------")
	print("29. Agent Runs to Fireball")
	print("30. Patient Walks to Fireball")
	print("31. Fireball Moving")
	print("32. Agent Saves Patient")
	print("------------GOOD SIMS----------------")
	print("33. Agent Saves Patient 1")
	print("34. Agent Makes Patient Safer")
	print("35. Agent Saves Patient 2")
	print("36. Dodge Save")
	print("0. EXIT")
	print("=================================================")
	print("Please choose a Simulation [1-14] or [0] to exit:")

def setBackground(screen):
	'''
	Sets the background for simulations. Expected screen
	of (1000px,600px).
	'''
	# top grass row
	screen.blit(BACKGROUND_S, (0,0))
	screen.blit(BACKGROUND_S, (200,0))
	screen.blit(BACKGROUND_S, (400,0))
	screen.blit(BACKGROUND_S, (600,0))
	screen.blit(BACKGROUND_S, (800,0))
	# bottom grass row
	screen.blit(BACKGROUND_S, (0,400))
	screen.blit(BACKGROUND_S, (200,400))
	screen.blit(BACKGROUND_S, (400,400))
	screen.blit(BACKGROUND_S, (600,400))
	screen.blit(BACKGROUND_S, (800,400))
	# sand row
	screen.blit(BACKGROUND_S, (0,200))
	screen.blit(BACKGROUND_S, (200,200))
	screen.blit(BACKGROUND_S, (400,200))
	screen.blit(BACKGROUND_S, (600,200))
	screen.blit(BACKGROUND_S, (800,200))

def wait(screen, space, options, cylinder, ball, cone):
	'''
	Creates a pause before any simulation runs if called
	'''
	pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
	pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
	pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)

	time=200
	while (time > 0):
			time-=1
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			setBackground(screen)
			screen.blit(fireSprite, pBall)
			screen.blit(patientSprite, pCone)
			screen.blit(agentSprite, pAgent)
			pygame.display.flip()

def snapshot(screen, counter):
	'''
	Takes a snapshot of a given frame in a pygame instance
	'''
	pygame.image.save(screen, "image"+str(counter)+".png")

def sample_trajectory():
	# Sample from normal distribution
	mu = 0
	sigma = 0.05
	return np.random.normal(mu, sigma)

import json

def serialize(c, data, filename='../example/test.json'):

	# dictionary of objects, each object has a list of dictionaries the length
	# of the number of frames, each dictionary has properties for that frame

	total_len = len(data['spaces'])

	objects = data['spaces'][0].bodies

	obj_data = {get_name(ob): [{} for _ in range(total_len)] for ob in objects}

	for n, frame in enumerate(data['spaces']):
		for ob in frame.bodies:

			ob_name = get_name(ob)

			obj_data[ob_name][n]['x'] = ob.position.x
			obj_data[ob_name][n]['y'] = ob.position.y


	container = {'config': c, 'data': obj_data}

	with open(filename, 'w') as f:
		json.dump(container, f, indent=2)

def get_name(ob):

	shape = ob.shapes.pop()
	return inverse_shape_code[shape.collision_type]

def get_position(ob_name, space):
	# we have to encode object identity in it's collision type, so to extract
	# it we need to check each object's type
	for ob in space.bodies:

		shape = ob.shapes.pop()

		# comparison must be == and not 'is'
		if shape.collision_type == shape_code[ob_name]:
			return ob.position

def get_velocity(ob_name, space):
	# we have to encode object identity in it's collision type, so to extract
	# it we need to check each object's type
	for ob in space.bodies:

		shape = ob.shapes.pop()

		# comparison must be == and not 'is'
		if shape.collision_type == shape_code[ob_name]:
			return ob.velocity
