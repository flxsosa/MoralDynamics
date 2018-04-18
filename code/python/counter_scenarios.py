'''
Set of scenarios used to counter the hypotheses posed in
Moral Kinematics 

Felix Sosa
'''
from environment import Environment
from planning import enumerate_policies
from handlers import rem0

def med_push_fireball(view=True,run=True,noise=[None,None],counter_tick=None):
	# Agent pushes fireball medium distance into patient
	# A - - F - - P
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
	p_params['moves'] = ['R','R','R','R','N']
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
	f_params['moves'] = ['R','R','R','R','N']
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

def push_patient_oncoming(view=True,run=True,noise=[None,None],counter_tick=None):
	# Agent pushes patient into oncoming fireball
	# A > > F < < P
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (100,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R','R','R','N','N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (500,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (900,300)
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

def push_fireball_oncoming(view=True,run=True,noise=[None,None],counter_tick=None):
	# Agent pushes against fireball into oncoming patient
	# A > > F < < P
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (100,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R','R','R','N','N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (900,300)
	p_params['color'] = "green"
	p_params['moves'] = ['L','L','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (500,300)
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

def fireball_walks_away(view=True,run=True,noise=[None,None],counter_tick=None):
	# Agent pushes patient into fireball moving away
	# A > F - P > >
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (100,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R','R','R','N','N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (300,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (500,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','R','R','N','N']
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

def patient_walks_away(view=True,run=True,noise=[None,None],counter_tick=None):
	# Agent pushes fireball into patient moving away
	# A > P - F > >
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (100,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R','R','R','N','N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (500,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','R','R','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (300,300)
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