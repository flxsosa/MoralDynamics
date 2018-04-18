from environment import Environment
from planning import enumerate_policies, run_policy
from handlers import rem0, rem1
from counterfactual import find_collision_tick, run_noisy_newton, run_csm

C = 'counter'
N = 'normal'
def long_distance(view=True,run=True,noise=[None,None],counter_tick=None):
	# Test two types of agents, good and bad in the scenario
	# A - - - P - F
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (100,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R','R','N','N', 'N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (300,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N', 'N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (800,300)
	f_params['color'] = "red"
	f_params['moves'] = ['L','L','L','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0),(1,0,rem1)]
	# Agent velocities
	vel = 300,150,150
	env = Environment(a_params,p_params,f_params,vel,handlers,view,noise,counter_tick)
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

print(run_csm(long_push_fireball_moving, True, [0,1],1))
