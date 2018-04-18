'''
Set of bad scenarios from fourth experiment

Felix Sosa
'''
from environment import Environment
from planning import enumerate_policies, run_policy
from handlers import rem0

def short_distance_fireball(view=True,run=True,noise=[None,None],counter_tick=None):
	# Test two types of agents, good and bad in the scenario
	# - - A - F - P
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (700,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R','N','N','N','N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (900,300)
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
	if run:
		env.configure()
		score = env.run()
	return env

def short_distance_patient(view=True,run=True,noise=[None,None],counter_tick=None):
	# Test two types of agents, good and bad in the scenario
	# - - A - P - F
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (700,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R','N','N','N','N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (800,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N','N']
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
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env

def push_against_fireball(view=True,run=True,noise=[None,None],counter_tick=None):
	# Agent pushes against fireball into patient
	# A < < F - - P
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (100,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R','R','R','R','R']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (900,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (500,300)
	f_params['color'] = "red"
	f_params['moves'] = ['L','L','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0)]
	# Agent velocities
	vel = 300,150,150
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env

def push_against_patient(view=True,run=True,noise=[None,None],counter_tick=None):
	# Agent pushes against patient into fireball
	# A < < P - - F
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (100,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R','R','R','R','R']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (500,300)
	p_params['color'] = "green"
	p_params['moves'] = ['L','L','N','N','N']
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
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env

def bystander_fireball(view=True,run=True,noise=[None,None],counter_tick=None):
	# Test two types of agents, good and bad in the scenario
	# - - - A - - -
	# F > > > > > P
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (500,500)
	a_params['color'] = "blue"
	a_params['moves'] = ['N','N','N','N','N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (900,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (100,300)
	f_params['color'] = "red"
	f_params['moves'] = ['R','R','R','R','R']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env

def bystander_patient(view=True,run=True,noise=[None,None],counter_tick=None):
	# Test two types of agents, good and bad in the scenario
	# - - - A - - -
	# P > > > > > F
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (500,500)
	a_params['color'] = "blue"
	a_params['moves'] = ['N','N','N','N','N']
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
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env

def long_push_fireball_moving(view=True,run=True,noise=[None,None],counter_tick=None):
	# Agent pushes walking fireball into patient
	# A - F > > > P
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (100,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R','R','R','R','R']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (900,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (300,300)
	f_params['color'] = "red"
	f_params['moves'] = ['R','R','R','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0)]
	# Agent velocities
	vel = 300,150,150
	patient_vel = 150
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env

def long_push_patient_moving(view=True,run=True,noise=[None,None],counter_tick=None):
	# Agent pushes walking patient into fireball
	# A - P > > > F
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (100,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R','R','R','R','R']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (300,300)
	p_params['color'] = "green"
	p_params['moves'] = ['R','R','R','N','N']
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
	patient_vel = 150
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env

def stays_put_fireball(view=True,run=True,noise=[None,None],counter_tick=None):
	# Test two types of agents, good and bad in the scenario
	# - - - - P - -
	# F > > A - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (500,250)
	a_params['color'] = "blue"
	a_params['moves'] = ['S','S','S','S','S']
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
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env

def stays_put_patient(view=True,run=True,noise=[None,None],counter_tick=None):
	# Test two types of agents, good and bad in the scenario
	# - - - - F - -
	# P > > A - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (500,250)
	a_params['color'] = "blue"
	a_params['moves'] = ['S','S','S','S','S']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (300,290)
	p_params['color'] = "green"
	p_params['moves'] = ['R','R','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (600,350)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env

def bump_fireball(view=True,run=True,noise=[None,None],counter_tick=None):
	# Test two types of agents, good and bad in the scenario
	# - - - A - - -
	# F > > | - - -
	# - - - - P - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (500,450)
	a_params['color'] = "blue"
	a_params['moves'] = ['N','N','D','N','N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (600,200)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (80,300)
	f_params['color'] = "red"
	f_params['moves'] = ['R','R','R','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env

def bump_patient(view=True,run=True,noise=[None,None],counter_tick=None):
	# Test two types of agents, good and bad in the scenario
	# - - - A - - -
	# P > > | - - -
	# - - - - F - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (500,450)
	a_params['color'] = "blue"
	a_params['moves'] = ['N','N','D','N','N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (80,300)
	p_params['color'] = "green"
	p_params['moves'] = ['R','R','R','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (600,200)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env