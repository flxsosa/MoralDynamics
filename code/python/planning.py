'''
Planning model for Moral Dynamics

Felix Sosa
'''
from itertools import product
import numpy as np
from environment import Environment

actions = ['R','L','U','D','N']

def enumerate_policies(num_actions, actions=actions):
	# Enumerate through all possible moves for a given number of actions
	return [', '.join(action) for action in product(actions, repeat=num_actions)]

def run_policy(a_params, p_params, f_params, vel, handlers):
	best_policy_score, best_policy = None, None
	for policy in enumerate_policies(5):
		print("== Performing Policy {} ==".format(policy))
		# Agent parameters
		a_params['moves'] = policy.split(', ')
		# Configure pygame and pymunk, run simulation, and score it
		env = Environment(a_params,p_params,f_params,vel,handlers,view=False)
		score = env.run()
		# Update best policy
		if score > best_policy_score or not best_policy_score:
			best_policy_score = score
			best_policy = policy.split(', ')
	print("Best policy: {0} with score {1}".format(best_policy,
												   best_policy_score))
	return best_policy_score, best_policy