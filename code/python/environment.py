'''
Class for agent environments in Moral Dynamics

Felix Sosa
'''
import sys
import pymunk
import pygame
import pymunk.pygame_util
from pygame.locals import *
import handlers
from agents import Agent, TypedAgent

class Environment:

	def __init__(self, a_params, p_params, f_params, vel, handlers=None, 
				 view=True, noise=[None,None], counter_tick=None, frict=0.05):
		# Agent params
		self.a_params, self.p_params, self.f_params = a_params, p_params, f_params
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
		# Pymunk space friction
		self.friction = frict
		# Agent velocities
		self.vel = vel
		# Engine parameters
		self.space = None
		self.screen = None
		self.options = None
		self.clock = None
		self.tick = 0
		self.counter_tick = [self.tick,counter_tick]
		self.noise = noise
		self.agent_collision = None
		self.patient_fireball_collision = 0
		# Collision handlers
		self.coll_handlers = [x for x in handlers] if handlers else handlers
		# Configure and run environment
		# self.configure()

	def configure(self,env_type='normal'):
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
		if env_type == 'normal': 
			self.space.add(self.agent.body, self.agent.shape,
						   self.patient.body, self.patient.shape,
						   self.fireball.body, self.fireball.shape)
		else:
			self.space.add(self.patient.body, self.patient.shape,
						   self.fireball.body, self.fireball.shape)
		print("Configured as {}".format(env_type))

	def run(self,run_type='normal'):
		# Run environment
		# Agent velocities
		a_vel, p_vel, f_vel = self.vel
		# Agent action generators (yield actions of agents)
		if run_type == 'normal':
			a_generator = self.agent.act(a_vel, self.clock, self.screen,
									self.space, self.options, self.view, 
									self.counter_tick, self.noise)
		p_generator = self.patient.act(p_vel, self.clock, self.screen,
								self.space, self.options, self.view, 
								self.counter_tick, self.noise)
		f_generator = self.fireball.act(f_vel, self.clock, self.screen,
								self.space, self.options, self.view, 
								self.counter_tick, self.noise)
		running = True
		# Run simulation until collision between P and F or policy ends
		while running and not handlers.PF_COLLISION:
			try:
				if run_type == 'normal':
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
				self.tick += 1
				if not handlers.A_COLLISION: self.agent_collision = self.tick
			except:
				running = False
		if self.view:
			pygame.quit()
			pygame.display.quit()
		# Record whether P and F collision occurred
		self.patient_fireball_collision = 1 if handlers.PF_COLLISION else 0
		# Reset collision handlers
		handlers.PF_COLLISION = []
		handlers.A_COLLISION = []
		# Return outcome to user (whether Agent's goal was reached or not)
		return self.agent.evaluate_policy(self.patient_fireball_collision)