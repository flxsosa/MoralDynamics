import pymunk
import pygame
import agents
import pymunk.pygame_util
from pygame.locals import *
import sys
import simulations
import infer
import sim
import matplotlib.pyplot as plt

def compareTotalImps():
	a = []
	c = range(14)
	b = ['shortDist',
		'medDist',
		'longDist',
		'static',
		'N/A',
		'N/A',
		'slowColl',
		'fastColl',
		'touch',
		'doubleTouch',
		'medPush',
		'longPush',
		'dodge',
		'pushFire']
	for i in range(14):
		# initialize pygame and create a space to contain the simulation
		pygame.init()
		space = pymunk.Space()

		# create a screen of 600x600 pixels
		screen = None
		drawOptions = None

		if (i == 0):
			a.append(sim.shortDistance(space, screen, drawOptions, True))
		elif (i == 1):
			a.append(sim.mediumDistance(space, screen, drawOptions, True))
		elif (i == 2):
			a.append(sim.longDistance(space, screen, drawOptions, True))
		elif (i == 3):
			a.append(sim.static(space, screen, drawOptions, True))
		elif (i == 4):
			a.append(0)
		elif (i == 5):
			a.append(0)
		elif (i == 6):
			a.append(sim.slowCollision(space, screen, drawOptions, True))
		elif (i == 7):
			a.append(sim.fastCollision(space, screen, drawOptions, True))
		elif (i == 8):
			a.append(sim.touch(space, screen, drawOptions, True))
		elif (i == 9):
			a.append(sim.doubleTouch(space, screen, drawOptions, True))
		elif(i == 10):
			a.append(sim.mediumPush(space, screen, drawOptions, True))
		elif (i == 11):
			a.append(sim.longPush(space, screen, drawOptions, True))
		elif (i == 12):
			a.append(sim.dodge(space, screen, drawOptions, True))
		elif (i == 13):
			a.append(sim.pushFireball(space, screen, drawOptions, True))
		pygame.quit()

	print(a,b)
	plt.bar(c,a)

	plt.xticks(c, b, rotation=50)
	plt.ylabel('Total Impulses')
	plt.title('Effort Comparison for Sims')
	plt.tight_layout()
	plt.savefig('comp.png')
	plt.show()

def compareKinematics():

	# empirical probabilities for each comparison in Moral Kinematics
	kinematics = [0.82, 0.88, 0.75, 0.5, 0.67, 0.84, 0.75,
				  1.0, 0.82, 0.75, 0.69, 0.75, 1.0, 0.82,
				  0.94]
	# calculated probabilities for each comparison in Moral Dynamics
	dynamics = calcProb()

	# x axis values for plot
	x = range(1, 16)
	xLabels = ['LongDist v ShortDist', 'LongDist v MedDist', 'LongDist v Static', 'MedPush v Down', 
			   'Up v Down', 'Up v MedPush', 'FastColl v SlowColl', 'Dodge v NoTouch',
			   'Dodge v Static', 'Static v NoTouch', 'LongDist v Dodge', 
			   'DoubleTouch v Touch', 'MedPush v Touch', 'LongPush v MedPush',
			   'LongPush v Touch']

	print kinematics, dynamics, xLabels

	plt.subplot(111)
	plt.ylabel("Agreement")
	plt.title("Moral Kinematics vs Moral Dynamics")
	plt.bar(x, kinematics, color='b')
	plt.bar(x, dynamics, color='r')
	plt.xticks(x, xLabels, rotation='70')
	plt.tight_layout()
	plt.show()

def calcProb():
	a = []
	prob = []

	# gather effort from each sim
	for i in range(14):
		# initialize pygame and create a space to contain the simulation
		pygame.init()
		space = pymunk.Space()

		# create a screen of 600x600 pixels
		screen = None
		drawOptions = None

		if (i == 0):
			a.append(sim.shortDistance(space, screen, drawOptions, True))
		elif (i == 1):
			a.append(sim.mediumDistance(space, screen, drawOptions, True))
		elif (i == 2):
			a.append(sim.longDistance(space, screen, drawOptions, True))
		elif (i == 3):
			a.append(sim.static(space, screen, drawOptions, True))
		elif (i == 4):
			a.append(0)
		elif (i == 5):
			a.append(0)
		elif (i == 6):
			a.append(sim.slowCollision(space, screen, drawOptions, True))
		elif (i == 7):
			a.append(sim.fastCollision(space, screen, drawOptions, True))
		elif (i == 8):
			a.append(sim.touch(space, screen, drawOptions, True))
		elif (i == 9):
			a.append(sim.doubleTouch(space, screen, drawOptions, True))
		elif(i == 10):
			a.append(sim.mediumPush(space, screen, drawOptions, True))
		elif (i == 11):
			a.append(sim.longPush(space, screen, drawOptions, True))
		elif (i == 12):
			a.append(sim.dodge(space, screen, drawOptions, True))
		elif (i == 13):
			a.append(sim.pushFireball(space, screen, drawOptions, True))
			pygame.quit()

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