'''
Set of good scenarios from fourth experiment

Felix Sosa
'''
from environment import Environment
from planning import enumerate_policies, run_policy
from handlers import rem0,rem1

def good_1(view=True,run=True,noise=[None,None],counter_tick=None):
	# Test two types of agents, good and bad in the scenario
	# F > > > A - P
	print("Good 1")
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (700,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['S','S','S','S', 'S']
	a_params['coll'] = 0
	a_params['type'] = 'G'
	# Patient parameters
	p_params['loc'] = (900,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N', 'N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (125,300)
	f_params['color'] = "red"
	f_params['moves'] = ['R','R','R','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0),(0,1,rem1),(0,2,rem1)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env

def good_2(view=True,run=True,noise=[None,None],counter_tick=None):
	# Test two types of agents, good and bad in the scenario
	# P > > > A - F
	print("Good 2")
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (700,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['S','S','S','S', 'S']
	a_params['coll'] = 0
	a_params['type'] = 'G'
	# Patient parameters
	p_params['loc'] = (125,300)
	p_params['color'] = "green"
	p_params['moves'] = ['R','R','R','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (900,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N', 'N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0),(0,1,rem1),(0,2,rem1)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env

def good_3(view=True,run=True,noise=[None,None],counter_tick=None):
	# Test two types of agents, good and bad in the scenario
	# P - A > < < F
	print("Good 3")
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (300,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['N','R','R','R', 'R']
	a_params['coll'] = 0
	a_params['type'] = 'G'
	# Patient parameters
	p_params['loc'] = (125,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N', 'N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (900,300)
	f_params['color'] = "red"
	f_params['moves'] = ['L','L','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0),(0,1,rem1),(0,2,rem1)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env

def good_4(view=True,run=True,noise=[None,None],counter_tick=None):
	# Test two types of agents, good and bad in the scenario
	# F - A > < < P
	print("Good 4")
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (300,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['N','R','R','R','R']
	a_params['coll'] = 0
	a_params['type'] = 'G'
	# Patient parameters
	p_params['loc'] = (900,300)
	p_params['color'] = "green"
	p_params['moves'] = ['L','L','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (125,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0),(0,1,rem1),(0,2,rem1)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env

def good_5(view=True,run=True,noise=[None,None],counter_tick=None):
	# Test two types of agents, good and bad in the scenario
	# - - - F - - -
	# P > - A - - -
	# - - - - - - -
	print("Good 5")
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (500,200)
	a_params['color'] = "blue"
	a_params['moves'] = ['N','U','N','N','N']
	a_params['coll'] = 0
	a_params['type'] = 'G'
	# Patient parameters
	p_params['loc'] = (125,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (500,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0),(0,1,rem1),(0,2,rem1)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env

def good_6(view=True,run=True,noise=[None,None],counter_tick=None):
	# Test two types of agents, good and bad in the scenario
	# - - - P - - -
	# F > - A - - -
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (500,200)
	a_params['color'] = "blue"
	a_params['moves'] = ['N','U','N','N','N']
	a_params['coll'] = 0
	a_params['type'] = 'G'
	# Patient parameters
	p_params['loc'] = (500,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (125,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0),(0,1,rem1),(0,2,rem1)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env

def good_7(view=True,run=True,noise=[None,None],counter_tick=None):
	# Test two types of agents, good and bad in the scenario
	# - - F < A - P
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (700,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['L','L','L','N', 'N']
	a_params['coll'] = 0
	a_params['type'] = 'G'
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
	handlers =[(1,2,rem0),(0,1,rem1),(0,2,rem1)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env

def good_8(view=True,run=True,noise=[None,None],counter_tick=None):
	# Test two types of agents, good and bad in the scenario
	# - - P < A - F
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (700,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['L','L','L','N', 'N']
	a_params['coll'] = 0
	a_params['type'] = 'G'
	# Patient parameters
	p_params['loc'] = (500,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (900,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0),(0,1,rem1),(0,2,rem1)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env

def good_9(view=True,run=True,noise=[None,None],counter_tick=None):
	# Test two types of agents, good and bad in the scenario
	# - - - P - - -
	# - - A | - - -
	# F > > | - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (440,400)
	a_params['color'] = "blue"
	a_params['moves'] = ['N','D','D','N','N']
	a_params['coll'] = 0
	a_params['type'] = 'G'
	# Patient parameters
	p_params['loc'] = (500,600)
	p_params['color'] = "green"
	p_params['moves'] = ['D','D','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (100,200)
	f_params['color'] = "red"
	f_params['moves'] = ['R','R','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0),(0,1,rem1),(0,2,rem1)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env

def good_10(view=True,run=True,noise=[None,None],counter_tick=None):
	# Test two types of agents, good and bad in the scenario
	# - - - F - - -
	# - - A | - - -
	# P > > | - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (440,400)
	a_params['color'] = "blue"
	a_params['moves'] = ['N','D','D','N','N']
	a_params['coll'] = 0
	a_params['type'] = 'G'
	# Patient parameters
	p_params['loc'] = (100,200)
	p_params['color'] = "green"
	p_params['moves'] = ['R','R','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (500,600)
	f_params['color'] = "red"
	f_params['moves'] = ['D','D','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0),(0,1,rem1),(0,2,rem1)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env

def good_11(view=True,run=True,noise=[None,None],counter_tick=None):
	# Test two types of agents, good and bad in the scenario
	# - A F > > - -
	# - - - ^ - - -
	# - - - P - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (180,500)
	a_params['color'] = "blue"
	a_params['moves'] = ['N','N','R','R','R']
	a_params['coll'] = 0
	a_params['type'] = 'G'
	# Patient parameters
	p_params['loc'] = (500,100)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','U','U','U']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (230,500)
	f_params['color'] = "red"
	f_params['moves'] = ['R','R','R','R','R']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0),(0,1,rem1),(0,2,rem1)]
	# Agent velocities
	vel = 300,300,150
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env

def good_12(view=True,run=True,noise=[None,None],counter_tick=None):
	# Test two types of agents, good and bad in the scenario
	# - A P > > - -
	# - - - ^ - - -
	# - - - F - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (180,500)
	a_params['color'] = "blue"
	a_params['moves'] = ['N','N','R','R','R']
	a_params['coll'] = 0
	a_params['type'] = 'G'
	# Patient parameters
	p_params['loc'] = (230,500)
	p_params['color'] = "green"
	p_params['moves'] = ['R','R','R','R','R']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (500,100)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','U','U','U']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0),(0,1,rem1),(0,2,rem1)]
	# Agent velocities
	vel = 300,150,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	if run:
		env.configure()
		score = env.run()
	return env