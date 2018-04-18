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
A_COLLISION = []
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

def rem1(arbiter, space, data):
	'''
	Used with post_solve. Removes the Cone after colliding with the Fireball.
	Expected that Cone is in space.shapes[1]
	'''
	if A_COLLISION:
		return True
	A_COLLISION.append(1)
	return True