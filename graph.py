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
simulations = [sim.shortDistance, sim.mediumDistance, sim.longDistance, sim.static,sim.uphill, 
			   sim.downhill, sim.slowCollision, sim.fastCollision, sim.touch, sim.doubleTouch, 
			   sim.mediumPush, sim.longPush, sim.dodge, sim.pushFireball]

def compareTotalImps():
	'''
	Plot total impulses applied to Agent for each of the 14 simulations.
	'''
	DYN = 1.0
	impulses = []
	idx = range(14)
	sims = ['shortDistance', 'medDistance', 'longDistance', 'static','N/A', 
		    'N/A', 'slowCollision', 'fastCollision', 'touch', 'doubleTouch', 
		    'medPush', 'longPush', 'dodge', 'pushFireball']
	
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
	plt.savefig('Dyn: '+ str(DYN) + '.png')
	plt.show()

def compareKinematics(DYN, flag=True):
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
		impulses.append(sim(space, screen, drawOptions, True, DYN))
		pygame.quit()

	# If a simulation failed at any time, do not account for it
	if None in impulses:
		print "Fail:"
	else:
		# probabilities using Luce's Choice Axiom
		dynamics = calcProb(impulses)
		# x axis values for plot
		idx = range(1, 16)
		xLabels = ['1. LongDist v ShortDist', '2. LongDist v MedDist', '3. LongDist v Static', '4. MedPush v Down', 
				   '5. Up v Down', '6. Up v MedPush', '7. FastColl v SlowColl', '8. Dodge v NoTouch',
				   '9. Dodge v Static', '10. Static v NoTouch', '11. LongDist v Dodge', 
				   '12. DoubleTouch v Touch', '13. MedPush v Touch', '14. LongPush v MedPush',
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
		plt.savefig('Dyn: '+ str(DYN) + 'kin.png')
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
	prob.append(a[2]/(a[1]+a[2]))
	# long distance vs static
	prob.append(a[2]/(a[3]+a[2]))
	# medium push vs downhill
	prob.append(0)
	# uphill vs downhill
	prob.append(0)
	# uphill vs medium push
	prob.append(0)
	# fast collision vs slow collision
	prob.append(a[7]/(a[6]+a[7]))
	# dodge vs no touch
	prob.append(1)
	# dodge vs static
	prob.append(a[12]/(a[3]+a[12]))
	# static vs no touch
	prob.append(1)
	# long distance vs dodge
	prob.append(a[2]/(a[12]+a[2]))
	# double touch vs touch
	prob.append(a[9]/(a[9]+a[8]))
	# medium push vs touch
	prob.append(a[10]/(a[10]+a[8]))
	# long push vs medium push
	prob.append(a[11]/(a[11]+a[10]))
	# long push vs touch
	prob.append(a[11]/(a[11]+a[8]))

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