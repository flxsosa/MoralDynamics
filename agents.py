'''
Classes of agents for Moral Dynamics.

March 14, 2016

Felix Sosa

Agent: the agent that acts to inflict harm on the patient. Cylinder in Moral Kinematics.
Patient: the agent that is harmed by the Agent. Cone in Moral Kinematics.
Fireball: object that is harful to Patient. Same in Moral Kinematics
'''

import pymunk
import pygame

class agent:
	'''
	A class for Agents in Moral Dynamics. 
	'''
	def __init__(self, x, y, rad=15):
		'''
		x -- x coordinate in pymunk space
		y -- y coordinate in pymunk space
		rad -- radius of shape
		'''
		self.body = pymunk.Body(1,1)
		self.body.position = (x,y)
		self.shape = pymunk.Circle(self.body, rad)
		self.shape.collision_type = 1
		self.shape.elasticity = 1

	def set(self, var, val):
		'''
		Set method for Agent.
		var -- attribute of Agent to set 
		val -- value to set attribute to
		'''
		if var=="imp":
			self.shape.body.apply_impulse_at_local_point(val)
		elif var=="frc":
			self.shape.body.apply_force_at_local_point(val, (0,0))
		elif var=="type" and val=="s":
			self.body = pymunk.Body(1,1, body_type=pymunk.Body.STATIC)
		elif var=="type" and val=="d":
			self.body = pymunk.Body(1,1, body_type=pymunk.Body.DYNAMIC)
			
class patient:
	'''
	A class for Patients in Moral Dynamics.
	'''
	def __init__(self, x, y, rad=15):
		'''
		x -- x coordinate in pymunk space
		y -- y coordinate in pymunk space
		rad -- radius of shape
		'''
		self.body = pymunk.Body(1,1)
		self.body.position = (x,y)
		self.shape = pymunk.Circle(self.body, rad)
		self.shape.color = pygame.color.THECOLORS["green"]
		self.shape.collision_type = 0
		self.shape.elasticity = 1

	def set(self, var, val):
		'''
		Set method for Patient.
		var -- attribute of Patient to set 
		val -- value to set attribute to
		'''
		if var=="imp":
			self.shape.body.apply_impulse_at_local_point(val)
		elif var=="frc":
			self.shape.body.apply_force_at_local_point(val, (0,0))
		elif var=="type" and val=="s":
			self.body = pymunk.Body(1,1, body_type=pymunk.Body.STATIC)
		elif var=="type" and val=="d":
			self.body = pymunk.Body(1,1, body_type=pymunk.Body.DYNAMIC)

class fireball:
	'''
	A class for Fireballs in Moral Dynamics.
	'''
	def __init__(self, x, y, rad=15):
		'''
		x -- x coordinate in pymunk space
		y -- y coordinate in pymunk space
		rad -- radius of shape
		'''
		self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
		self.body.position = x,y 
		self.shape = pymunk.Circle(self.body, rad)
		self.shape.color = pygame.color.THECOLORS["red"]
		self.shape.collision_type = 2