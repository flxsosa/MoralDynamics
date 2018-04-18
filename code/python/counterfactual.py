'''
General functions for running counterfactuals in Pymunk

Felix Sosa
'''
from itertools import product
import numpy as np
from environment import Environment

def find_collision_tick(environment, env_type, run_type):
	# Find tick in simulation in which desired collision occurs
	environment.configure(env_type)
	print("Running Environment")
	environment.run(run_type)
	print("Collision Tick: {}".format(environment.agent_collision))
	return environment.agent_collision

def run_noisy_newton(environment,view,noise,collision_tick):
	# Run a simulation noisily given noise parameters, 
	# and tick to start from
	print("Noise: {}".format(noise))
	env = Environment(environment.a_params, environment.p_params,
					  environment.f_params, environment.vel, 
					  environment.coll_handlers, view, 
					  noise, collision_tick)
	env.configure('counter')
	env.run('counter')
	return env

def run_csm(environment,view,noise,num_times):
	# Run a counterfactual simulation
	print("Declaring Environment")
	normal_env = environment(view,False)
	print("Gathering Collision Tick")
	collision = find_collision_tick(normal_env, 'normal', 'normal')
	prob_cause = 0.0
	for _ in range(num_times):
		counter_env = run_noisy_newton(normal_env, view, noise, collision)
		print("Normal: {}".format(normal_env.patient_fireball_collision))
		print("Counter: {}".format(counter_env.patient_fireball_collision))
		prob_cause += int(not(normal_env.patient_fireball_collision == 
							  counter_env.patient_fireball_collision))
	return prob_cause/num_times