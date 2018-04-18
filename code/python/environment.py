'''
Class for agent environments in Moral Dynamics

Felix Sosa
'''
import pymunk
import pygame
import pymunk.pygame_util
from pygame.locals import *
import handlers
from agents import Agent, TypedAgent

class Environment:

	def __init__(self, a_params, p_params, f_params, vel, handlers=None, 
				 view=True, e_noise=0, a_noise=0, frict=0.05):
		# Boolean flag for whether you want to view the sim or not
		self.view = view
		# Objects in environent
		self.agent = TypedAgent(a_params['loc'][0], a_params['loc'][1], 
						   a_params['color'], a_params['coll'], 
						   a_params['moves'], a_params['type'])
		self.patient = Agent(p_params['loc'][0], p_params['loc'][1], 
							 p_params['color'], p_params['coll'], 
							 p_params['moves'])
		self.fireball = Agent(f_params['loc'][0], f_params['loc'][1], 
							  f_params['color'], f_params['coll'], 
							  f_params['moves'])
		# Initial location of objects in environment
		self.p_loc = p_params['loc']
		self.a_loc = a_params['loc']
		self.f_loc = f_params['loc']
		# Environement and agent parameters
		self.e_noise = e_noise
		self.a_noise = a_noise
		# Pymunk space friction
		self.friction = frict
		# Agent velocities
		self.vel = vel
		# Engine parameters
		self.space = None
		self.screen = None
		self.options = None
		self.clock = None
		# Collision handlers
		self.coll_handlers = [x for x in handlers] if handlers else handlers
		# Configure and run environment
		self.configure()

	def configure(self):
		# Configure pymunk space and pygame engine parameters (if any)
		if self.view:
			pygame.init()
			self.screen = pygame.display.set_mode((1000,600))
			self.options = pymunk.pygame_util.DrawOptions(self.screen)
			self.clock = pygame.time.Clock()
		self.space = pymunk.Space()
		self.space.damping = self.friction
		# Configure collision handlers if there are any
		if self.coll_handlers:
			for ob1, ob2, rem in self.coll_handlers:
				ch = self.space.add_collision_handler(ob1, ob2)
				ch.data["surface"] = self.screen
				ch.post_solve = rem
		# Add agents to the pymunk space
		self.space.add(self.agent.body, self.agent.shape,
					   self.patient.body, self.patient.shape,
					   self.fireball.body, self.fireball.shape)

	def run(self):
		# Run environment
		# Agent velocities
		a_vel, p_vel, f_vel = self.vel
		# Agent action generators (yield actions of agents)
		a_generator = self.agent.act(a_vel, self.clock, self.screen,
								self.space, self.options, self.view)
		p_generator = self.patient.act(p_vel, self.clock, self.screen,
								self.space, self.options, self.view)
		f_generator = self.fireball.act(f_vel, self.clock, self.screen,
								self.space, self.options, self.view)
		running = True
		# Run simulation until collision between P and F or policy ends
		while running and not handlers.PF_COLLISION:
			try:
				next(a_generator)
				next(p_generator)
				next(f_generator)
				# Render space if requested
				if self.view:
					self.screen.fill((255,255,255))
					self.space.debug_draw(self.options)
					pygame.display.flip()
					self.clock.tick(50)
				self.space.step(1/50.0)
			except:
				running = False
		if self.view:
			pygame.quit()
			pygame.display.quit()
		# Record whether P and F collision occurred
		coll = 1 if handlers.PF_COLLISION else 0
		# Reset collision handler
		handlers.PF_COLLISION = []
		# Return outcome to user (whether Agent's goal was reached or not)
		return self.agent.evaluate_policy(coll)