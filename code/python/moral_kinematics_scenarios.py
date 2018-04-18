'''
Set of scenarios from Moral Kinematics that can be replicated
with Pymunk and Pygame

Felix Sosa
'''
from environment import Environment
from planning import enumerate_policies, run_policy
from handlers import rem0, rem2, rem4

def long_distance(view=True):
	# Test two types of agents, good and bad in the scenario
	# A - - - P - F
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (100,300)
	a_params['color'] = "blue"
	a_params['moves'] = None
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (800,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N', 'N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (900,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0)]
	# Agent velocities
	vel = 300,150,150
	# Enumerate and score agent's possible policies
	best_policy_score, best_policy = run_policy(a_params, p_params, 
												f_params, vel, handlers)
	a_params['moves'] = best_policy
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	score = env.run()
	return env.agent.effort_expended

def dodge(view=True):
	# Test two types of agents, good and bad in the scenario
	# P > > A - - F
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (500,300)
	a_params['color'] = "blue"
	a_params['moves'] = None
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (100,300)
	p_params['color'] = "green"
	p_params['moves'] = ['R','R','R','R','R']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (900,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	# Enumerate and score agent's possible policies
	best_policy_score, best_policy = run_policy(a_params, p_params, 
												f_params, vel, handlers)
	a_params['moves'] = best_policy if best_policy else ['N']*5
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	score = env.run()
	return env.agent.effort_expended

def bystander(view=True):
	# Test two types of agents, good and bad in the scenario
	# - - - A - - -
	# P > > > > > F
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (500,500)
	a_params['color'] = "blue"
	a_params['moves'] = None
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (100,300)
	p_params['color'] = "green"
	p_params['moves'] = ['R','R','R','R','R']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (900,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	# Enumerate and score agent's possible policies
	best_policy_score, best_policy = run_policy(a_params, p_params, 
												f_params, vel, handlers)
	a_params['moves'] = best_policy if best_policy else ['N']*5
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	score = env.run()
	return env.agent.effort_expended

def stays_put(view=True):
	# Test two types of agents, good and bad in the scenario
	# - - - - P - -
	# F > > A - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (500,250)
	a_params['color'] = "blue"
	a_params['moves'] = None
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (600,350)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (300,290)
	f_params['color'] = "red"
	f_params['moves'] = ['R','R','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	# Enumerate and score agent's possible policies
	best_policy_score, best_policy = run_policy(a_params, p_params, 
												f_params, vel, handlers)
	a_params['moves'] = best_policy if best_policy else ['N']*5
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	score = env.run()
	return env.agent.effort_expended

def short_distance(view=True):
	# Test two types of agents, good and bad in the scenario
	# - - A - P - F
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (600,300)
	a_params['color'] = "blue"
	a_params['moves'] = None
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (800,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N', 'N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (900,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	# Enumerate and score agent's possible policies
	best_policy_score, best_policy = run_policy(a_params, p_params, 
												f_params, vel, handlers)
	a_params['moves'] = best_policy
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	score = env.run()
	return env.agent.effort_expended

def med_push(view=True):
	# Test two types of agents, good and bad in the scenario
	# A - - P - - F
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (100,300)
	a_params['color'] = "blue"
	a_params['moves'] = None
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (500,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N', 'N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (900,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	# Enumerate and score agent's possible policies
	best_policy_score, best_policy = run_policy(a_params, p_params, 
												f_params, vel, handlers)
	a_params['moves'] = best_policy
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	score = env.run()
	return env.agent.effort_expended

def long_push(view=True):
	# Test two types of agents, good and bad in the scenario
	# A P - - - - F
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (100,300)
	a_params['color'] = "blue"
	a_params['moves'] = None
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (200,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N', 'N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (900,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	# Enumerate and score agent's possible policies
	best_policy_score, best_policy = run_policy(a_params, p_params, 
												f_params, vel, handlers)
	a_params['moves'] = best_policy
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	score = env.run()
	return env.agent.effort_expended

def push_patient(view=True):
	# Test two types of agents, good and bad in the scenario
	# - F - - - - -
	# - - - < < < P
	# - - - A - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	# a_params['loc'] = (550,100) # <- check this out
	a_params['loc'] = (500,100)
	a_params['color'] = "blue"
	a_params['moves'] = None
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	# p_params['loc'] = (900,300) # <- check this out
	p_params['loc'] = (900,300)
	p_params['color'] = "green"
	p_params['moves'] = ['L','L','N','N', 'N']
	p_params['coll'] = 1
	# Fireball parameters
	# f_params['loc'] = (450,500) # <- check this out
	f_params['loc'] = (450,500)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	# Enumerate and score agent's possible policies
	best_policy_score, best_policy = run_policy(a_params, p_params, 
												f_params, vel, handlers)
	a_params['moves'] = best_policy
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	score = env.run()
	return env.agent.effort_expended

def double_push(view=True):
	# Test two types of agents, good and bad in the scenario
	# A P - - - - F
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (200,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R','S','R','R','R']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (300,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (800,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	score = env.run()
	return env.agent.effort_expended