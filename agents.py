'''
Agent Classes for Moral Dynamics.

March 14, 2016
Felix Sosa
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
		self.body = pymunk.Body(1,1)
		# self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
		self.body.position = x,y 
		self.shape = pymunk.Circle(self.body, rad)
		self.shape.color = pygame.color.THECOLORS["red"]
		self.shape.collision_type = 2
		self.shape.elasticity = 0