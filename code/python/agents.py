'''
Agent Classes for Moral Dynamics.

March 14, 2017
Felix Sosa
'''
import pymunk
import pygame
import glob
# Distance agents move per action
move_lat_distance = 160
move_long_distance = 160
wait_period = 27

class Agent:

	def __init__(self, x, y, color, collision, moves, mass=1, rad=25):
		# Actions available to agents
		action_dict = {
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
		self.actions = [action_dict[x] for x in moves]
	
	def noisy_action(action, action_probability):
		if numpy.random.uniform() < action_probability:
			return action
		return np.random.choice(action_dict.values())

	def move_right(self, velocity, clock, screen, space, options, view):
		# Move agent right
		intended_x_pos = self.body.position[0]+move_lat_distance
		while self.body.position[0] < intended_x_pos:
			if view:
				for event in pygame.event.get():
					pass
			if self.body.velocity[0] < velocity:
				imp = velocity - self.body.velocity[0]
				self.body.apply_impulse_at_local_point((imp,0))
				self.effort_expended += imp
			yield

	def move_left(self, velocity, clock, screen, space, options, view):
		# Move agent left
		intended_x_pos = self.body.position[0]-move_lat_distance
		while self.body.position[0] > intended_x_pos:
			if view:
				for event in pygame.event.get():
					pass
			if abs(self.body.velocity[0]) < velocity:
				imp = velocity - abs(self.body.velocity[0])
				self.body.apply_impulse_at_local_point((-1*imp,0))
				self.effort_expended += imp
			yield

	def move_up(self, velocity, clock, screen, space, options, view):
		# Move agent up
		intended_y_pos = self.body.position[1]+move_long_distance
		while self.body.position[1] < intended_y_pos:
			if view:
				for event in pygame.event.get():
					pass
			if self.body.velocity[1] < velocity:
				imp = velocity - self.body.velocity[1]
				self.body.apply_impulse_at_local_point((0,imp))
				self.effort_expended += imp
			yield

	def move_down(self, velocity, clock, screen, space, options, view):
		# Move agent up
		intended_y_pos = self.body.position[1]-move_long_distance
		while self.body.position[1] > intended_y_pos:
			if view:
				for event in pygame.event.get():
					pass
			if abs(self.body.velocity[1]) < velocity:
				imp = velocity - abs(self.body.velocity[1])
				self.body.apply_impulse_at_local_point((0,-1*imp))
				self.effort_expended += imp
			yield
	
	def do_nothing(self, velocity, clock, screen, space, options, view):
		# Move agent up
		for _ in range(wait_period):
			if view:
				for event in pygame.event.get():
					pass
			yield

	def stay_put(self, velocity, clock, screen, space, options, view):
		# Move agent up
		for _ in range(wait_period):
			if view:
				for event in pygame.event.get():
					pass
				if abs(self.body.velocity[1]) > 0:
					imp = -1*self.body.velocity[1]
					self.body.apply_impulse_at_local_point((0,imp))
					self.effort_expended += abs(imp)
				if abs(self.body.velocity[0]) > 0:
					imp = -1*self.body.velocity[0]
					self.body.apply_impulse_at_local_point((imp,0))
					self.effort_expended += abs(imp)
			yield

	def act(self, velocity, clock, screen, space, options, view):
		# Execute policy
		actions = iter(self.actions)
		actions_left = True
		action = next(actions)
		while actions_left:
			try:
				for _ in action(velocity, clock, screen, space, options, view):
					yield
				action = next(actions)
			except:
				return
		
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
		print("Goal: {}".format(self.type))
		print(("Did" if ach_goal else "Did not") + " achieve goal.")
		print("Reward for achieving goal: {}".format(self.reward))
		print("Effort Expended: {}".format(self.effort_expended))
		print("Utility: {}".format(ach_goal*self.reward - self.effort_expended))
		print("Score for Policy: {}\n".format((ach_goal*self.reward-
											 self.effort_expended)/
											 self.reward))
		return ((ach_goal*self.reward - self.effort_expended)/self.reward)