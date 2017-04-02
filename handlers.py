'''
Collision Handlers for MoralDynamics

April 2, 2017
Felix Sosa
'''
import pygame
import pymunk
from pygame.locals import *

def rem0(arbiter, space, data):
	'''
	Used with post_solve. Removes the Cone after colliding with the Fireball.
	Expected that Cone is in space.shapes[1]
	'''
	space.remove(space.shapes[1])
	running = False
	pygame.time.set_timer(QUIT, 1000)
	return True

def rem1(arbiter, space, data):
	'''
	Used with post_solve. Causes cone to travel slower after being hit by Cylinder.
	'''
	space.shapes[1].body.velocity = \
	(space.shapes[1].body.velocity[0]/2.5, 
		space.shapes[1].body.velocity[1]/2.5)
	space.shapes[2].body.velocity=(0,0)
	return True

def rem2(arbiter, space, data):
	'''
	Used with begin method of CollisionHandler. Adds element to collision list
	to signify a collision has begun.
	'''
	collision.append(1)
	return True