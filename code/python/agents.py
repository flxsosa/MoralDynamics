'''
Agent Classes for Moral Dynamics.

March 14, 2017
Felix Sosa
'''
import sys
import pymunk
import pygame
import glob
from numpy.random import normal as gauss
import numpy as np
# from planning import noisy_policy

# Distance agents move per action
move_lat_distance = 160
move_long_distance = 160
wait_period = 27
action_noise = 0.9

class Agent:

	def __init__(self, x, y, color, collision, moves, mass=1, rad=25):
		# Actions available to agents
		self.action_dict = {
			'U':self.move_up,
			'D':self.move_down,
			'R':self.move_right,
			'L':self.move_left,
			'N':self.do_nothing,
			'S':self.stay_put
		}
		# Agent attributes
		self.body = pymunk.Body(mass,1)
		self.body.position = (x,y)
		self.shape = pymunk.Circle(self.body, rad)
		self.shape.color = pygame.color.THECOLORS[color]
		self.shape.collision_type = collision
		self.shape.elasticity = 1
		self.effort_expended = 0
		self.actions = [self.action_dict[x] for x in moves]
		self.moves = moves

	def move_right(self,velocity,clock,screen,space,options,view,t,n):
		# Move agent right
		intended_x_pos = self.body.position[0]+move_lat_distance
		while self.body.position[0] < intended_x_pos:
			if view:
				for event in pygame.event.get():
					pass
			if self.body.velocity[0] < velocity:
				imp = velocity - self.body.velocity[0]
				noise = 0
				if t[1]: noise = gauss(n[0],n[1]) if t[0] >= t[1] else 0
				self.body.apply_impulse_at_local_point((imp,imp*noise))
				self.effort_expended += imp
			yield

	def move_left(self,velocity,clock,screen,space,options,view,t=None,n=None):
		# Move agent left
		intended_x_pos = self.body.position[0]-move_lat_distance
		while self.body.position[0] > intended_x_pos:
			if view:
				for event in pygame.event.get():
					pass
			if abs(self.body.velocity[0]) < velocity:
				imp = velocity - abs(self.body.velocity[0])
				noise = 0
				if t[1]: noise = gauss(n[0],n[1]) if t[0] >= t[1] else 0
				self.body.apply_impulse_at_local_point((-1*imp,imp*noise))
				self.effort_expended += imp
			yield

	def move_up(self,velocity,clock,screen,space,options,view,t=None,n=None):
		# Move agent up
		intended_y_pos = self.body.position[1]+move_long_distance
		while self.body.position[1] < intended_y_pos:
			if view:
				for event in pygame.event.get():
					pass
			if self.body.velocity[1] < velocity:
				imp = velocity - self.body.velocity[1]
				noise = 0
				if t[1]: noise = gauss(n[0],n[1]) if t[0] >= t[1] else 0
				self.body.apply_impulse_at_local_point((imp*noise,imp))
				self.effort_expended += imp
			yield

	def move_down(self,velocity,clock,screen,space,options,view,t=None,n=None):
		# Move agent up
		intended_y_pos = self.body.position[1]-move_long_distance
		while self.body.position[1] > intended_y_pos:
			if view:
				for event in pygame.event.get():
					pass
			if abs(self.body.velocity[1]) < velocity:
				imp = velocity - abs(self.body.velocity[1])
				noise = 0
				if t[1]: noise = gauss(n[0],n[1]) if t[0] >= t[1] else 0
				self.body.apply_impulse_at_local_point((imp*noise,-1*imp))
				self.effort_expended += imp
			yield
	
	def do_nothing(self,velocity,clock,screen,space,options,view,t=None,n=None):
		# Move agent up
		for _ in range(wait_period):
			if view:
				for event in pygame.event.get():
					pass
			yield

	def stay_put(self,velocity,clock,screen,space,options,view,t=None,n=None):
		# Move agent up
		for _ in range(wait_period):
			if view:
				for event in pygame.event.get():
					pass
			if abs(self.body.velocity[1]) > 0:
				imp = -1*self.body.velocity[1]
				noise = 0
				if t[1]: noise = gauss(n[0],n[1]) if t[0] >= t[1] else 0
				self.body.apply_impulse_at_local_point((imp*noise,imp))
				self.effort_expended += abs(imp)
			if abs(self.body.velocity[0]) > 0:
				imp = -1*self.body.velocity[0]
				noise = 0
				if t[1]: noise = gauss(n[0],n[1]) if t[0] >= t[1] else 0
				self.body.apply_impulse_at_local_point((imp,imp*noise))
				self.effort_expended += abs(imp)
			yield

	def act(self,velocity,clock,screen,space,options,view,t,n):
		# Execute policy
		if n[1]:
			timepoint = t[1]/wait_period
			print("T[1]: {} wait_period {}".format(t[1], wait_period))
			noisy = self.sticky_policy(self.moves,timepoint)
			noisy_actions = [self.action_dict[x] for x in noisy]
			if(len(noisy_actions) == 5):
				raise ValueError("Bruh")
			actions = iter(noisy_actions)
		else:
			actions = iter(self.actions)
		actions_left = True
		action = next(actions)
		while actions_left:
			try:
				for _ in action(velocity,clock,screen,space,options,view,t,n):
					if t[1]: t[0]+=1
					yield
				action = next(actions)
			except:
				return

	def noisy_policy(self, policy, timepoint=0):
		if timepoint >= 5:
			return policy
		try:
			curr_policy = policy.split(', ')
		except:
			curr_policy = policy
		for i in range(len(curr_policy)):
			if np.random.uniform() < action_noise and i >= timepoint:
				curr_policy[i] = np.random.choice(['R','L','N','U','D'])
		return curr_policy

	def sticky_policy(self, policy, timepoint=0):
		print("Original Policy: {}".format(policy))
		print("Timepoint: {}".format(timepoint))
		if timepoint >= 5:
			return policy

		try:
			curr_policy = [x for x in policy.split(', ')]
		except:
			curr_policy = [x for x in policy]

		if timepoint == 0:
			sticky_action = curr_policy[timepoint]
		else:
			sticky_action = curr_policy[timepoint-1]
			
		for i in range(len(curr_policy)):
			if i >= timepoint-1:
				curr_policy[i] = sticky_action
		curr_policy.extend([sticky_action,sticky_action])
		print("Sticky Policy: {}".format(curr_policy))
		return curr_policy
		
class Goals:

	def __init__(self, goal_type, reward=10000):
		self.type = goal_type
		self.reward = reward if self.type else 1

	def check_goal(self, goal_type, pf_coll):
		if goal_type == 'G' and not pf_coll: return 1
		elif goal_type == 'B' and pf_coll: return 1
		else: return 0

class TypedAgent(Goals,Agent):
	
	def __init__(self, x, y, color, collision, moves, goal_type):
		Goals.__init__(self,goal_type)
		Agent.__init__(self,x, y, color, collision, moves)
		self.utility = 0

	def evaluate_policy(self, pf_coll):
		# See whether agent achieved its goal or not and return corresponding
		# utility
		ach_goal = self.check_goal(self.type, pf_coll)
		# print("Goal: {}".format(self.type))
		# print(("Did" if ach_goal else "Did not") + " achieve goal.")
		# print("Reward for achieving goal: {}".format(self.reward))
		# print("Effort Expended: {}".format(self.effort_expended))
		# print("Utility: {}".format(ach_goal*self.reward - self.effort_expended))
		# print("Score for Policy: {}\n".format((ach_goal*self.reward-
		# 									 self.effort_expended)/
		# 									 self.reward))
		return ((ach_goal*self.reward - self.effort_expended)/self.reward)