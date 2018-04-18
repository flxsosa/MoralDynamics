'''
Collision Handlers for Moral Dynamics

April 2, 2017
Felix Sosa
'''
import pygame
import pymunk
from pygame.locals import *

collision = []
PF_COLLISION = []
totalImpulse = []

def rem0(arbiter, space, data):
	'''
	Used with post_solve. Removes the Cone after colliding with the Fireball.
	Expected that Cone is in space.shapes[1]
	'''
	if PF_COLLISION:
		return True
	space.remove(space.shapes[1])
	space.remove(space.bodies[1])
	running = False
	PF_COLLISION.append(1)
	pygame.time.set_timer(QUIT, 1000)
	return True

def rem2(arbiter, space, data):
	'''
	Used with begin method of CollisionHandler. Adds element to collision list
	to signify a collision has begun.
	'''
	collision.append(1)
	return True

def rem4(arbiter, space, data):
	'''
	Used with begin method of CollisionHandler. Adds element to collision list
	to signify a collision has begun.
	'''
	PF_COLLISION = 1
	return True