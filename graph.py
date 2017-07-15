'''
Graphing functions for Moral Dynamics.

Felix Sosa
March 25, 2017
'''

import pymunk
import pygame
import pymunk.pygame_util
from pygame.locals import *
import sim
import matplotlib.pyplot as plt

# list of simulation calls from sim.py to be passed as parameters
simulations = [sim.shortDistancev1, sim.mediumDistancev1, sim.longDistancev1, sim.static,
			   sim.slowCollision, sim.fastCollision, sim.noTouch, sim.doublePush, 
			   sim.mediumPush, sim.longPush, sim.dodge, sim.pushFireball, sim.mediumDistancev2,
			   sim.longDistancev2, sim.victim_moving_static]

def compareTotalImps():
	'''
	Plot total impulses applied to Agent for each of the 14 simulations.
	'''
	impulses = []
	idx = range(15)
	sims = ['shortDistancev1', 'mediumDistancev1', 'longDistancev1', 'static',
			   'slowCollision', 'fastCollision', 'noTouch', 'doublePush', 
			   'mediumPush', 'longPush', 'dodge', 'pushFireball', 'mediumDistancev2',
			   'longDistancev2', 'moving']
	
	# traverse simulations and 
	for sim in simulations:
		# initialize pygame and create a space to contain the simulation
		pygame.init()
		space = pymunk.Space()
		# we are not viewing the sims
		screen = None
		drawOptions = None
		# append total impulse applied to Agent for given simulation
		impulses.append(sim(space, screen, drawOptions, True))
		pygame.quit()

	# create bar graph of total impulses per simulation
	plt.bar(idx,impulses)
	plt.xticks(idx, sims, rotation=50)
	plt.ylabel('Total Impulses')
	plt.title('Effort Comparison for Sims')
	plt.tight_layout()
	plt.savefig('NewSims' + '.png')
	plt.show()

def compareKinematics(flag=True):
	'''
	Plots two bar plots. One for Moral Kinematics data and one for
	Moral Dynamics data.
	'''
	# impulses
	impulses = []
	# agreements for each comparison in Moral Kinematics
	kinematics = [0.82, 0.88, 0.75, 0.5, 0.67, 0.84, 0.75, 1.0, 
				  0.82, 0.75, 0.69, 0.75, 1.0, 0.82, 0.94]
	# calculated probabilities for each comparison in Moral Dynamics
	print "Gathering data..."

	# traverse simulations and append impulses to list
	for sim in simulations:
		# initialize pygame and create a space to contain the simulation
		pygame.init()
		space = pymunk.Space()
		# we are not viewing the sims
		screen = None
		drawOptions = None
		# append total impulse applied to Agent for given simulation
		impulses.append(sim(space, screen, drawOptions, True))
		pygame.quit()

	# If a simulation failed at any time, do not account for it
	if None in impulses:
		print "Fail:"
	else:
		# probabilities using Luce's Choice Axiom
		dynamics = calcProb(impulses)
		# x axis values for plot
		idx = range(1, 16)
		xLabels = ['1. LongDistv1 v ShortDistv1', '2. LongDistv2 v MedDistv2', '3. Movingt v Static', '4. MedPush v Down', 
				   '5. Up v Down', '6. Up v MedPush', '7. FastColl v SlowColl', '8. Dodge v NoTouch',
				   '9. Dodge v Static', '10. Static v NoTouch', '11. Moving v Dodge', 
				   '12. LongPush v DoublePush', '13. MedDistv2 v MedPush', '14. LongPush v MedPush',
				   '15. LongPush v Touch']

		# double bar plot
		plt.subplot(111)
		plt.ylabel("Agreement")
		plt.title("Moral Kinematics vs Moral Dynamics")
		# Moral Kinematics data
		plt.bar(idx, kinematics, width=0.2, color='b', label='Kin')
		# Moral Dynamics data - need to plot bars next to Kinematics bars
		plt.bar(map(lambda x:x+0.2, idx), dynamics, width=0.2, color='r', label='Dyn')
		plt.xticks(idx, xLabels, rotation='70')
		plt.legend(loc="best")
		plt.plot([0.5]*17, "k--")
		plt.tight_layout()
		plt.savefig('kin.png')
		plt.show()

def calcProb(a):
	'''
	Calculate probability one simulation would be deemed worse than another
	using Luce's Choice Theorem. Currently calculates probabilities of the
	same situations presented in Moral Kinematics by Iliev et. al, 2012.
	'''
	prob = []

	# long distance vs short distance
	prob.append(a[2]/(a[0]+a[2]))
	# long distance vs medium distance
	prob.append(a[13]/(a[12]+a[13]))
	# long distance vs static
	prob.append(a[14]/(a[3]+a[14]))
	# medium push vs downhill
	prob.append(0)
	# uphill vs downhill
	prob.append(0)
	# uphill vs medium push
	prob.append(0)
	# fast collision vs slow collision
	prob.append(a[5]/(a[5]+a[4]))
	# dodge vs no touch
	prob.append(a[10]/(a[10]+a[6]))
	# dodge vs static
	prob.append(a[10]/(a[3]+a[10]))
	# static vs no touch
	prob.append(a[3]/(a[3]+a[6]))
	# Moving vs dodge
	prob.append(a[14]/(a[14]+a[10]))
	# Long Push vs Double Push
	prob.append(a[7]/(a[9]+a[7]))
	# Medium Distance v2 vs Medium Push
	prob.append(a[8]/(a[12]+a[8]))
	# long push vs medium push
	prob.append(a[9]/(a[9]+a[8]))
	# long push vs touch
	prob.append(a[9]/(a[9]+a[2]))

	return prob

def modelFit():
	'''
	Model fit using model parameters.
	'''	
	# agreements for each comparison in Moral Kinematics
	kinematics = [0.82, 0.88, 0.75, 0.0, 0.0, 0.0, 0.75, 1.0, 
				  0.82, 0.75, 0.69, 0.75, 1.0, 0.82, 0.94]
	# value dictionary
	values = {"Value" : "DYN"}

	for dyn in range(30,101):

		impulses = []
		for sim in simulations:
			# initialize pygame and create a space to contain the simulation
			pygame.init()
			space = pymunk.Space()
			# we are not viewing the sims
			screen = None
			drawOptions = None
			# append total impulse applied to Agent for given simulation
			impulses.append(sim(space, screen, drawOptions, True, dyn*0.01))
			pygame.quit()
		# If a simulation failed, do not account for it
		if None in impulses:
			print "=============================="
			print "Fail at Dynamic Friction: ", dyn*0.1
			print "=============================="
		else:
			dynamics = calcProb(impulses)
			print "=============================="
			print "Success at Dynamic Friction: ", dyn*0.1
			values[dyn*0.1] = rmse(kinematics, dynamics)
			print "=============================="
	# print the values of the dict
	print min(values, key=values.get)

def rmse(x, y):
	'''
	Root mean squared error between two lists of numbers.
	'''
	z = []

	for i in range(len(x)):
		z.append((x[i] - y[i])**2)

	square = sum(z)/(len(x)+0.0)
	return square**0.5