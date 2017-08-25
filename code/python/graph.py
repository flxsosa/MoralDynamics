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
import sqlite3
from scipy import stats
import numpy as np

# list of simulation calls from sim.py to be passed as parameters
simulations = [sim.shortDistancev1,sim.mediumDistancev2,sim.longDistancev1,
				sim.static,sim.slowCollision,sim.fastCollision,sim.dodge,
				sim.doublePush,sim.mediumPush,sim.longPush,sim.victim_moving_static,
				sim.noTouch,sim.victim_moving_moving,sim.victim_moving_static,
				sim.victim_static_moving,sim.victim_static_static,sim.harm_moving_moving,
				sim.harm_moving_static,sim.harm_static_moving,sim.harm_static_static,sim.sim1Patient,
				sim.sim1Fireball,sim.sim2Patient,sim.sim2Fireball,sim.sim3Patient,
				sim.sim3Fireball,sim.sim4Patient,sim.sim4Fireball]

def compareTotalImps():
	'''
	Plot total impulses applied to Agent for each of the 14 sim.
	'''
	impulses = []
	idx = range(28)
	sims = ['shortDistancev1','mediumDistancev2','longDistancev1',
				'static','slowCollision','fastCollision','dodge',
				'doublePush','mediumPush','longPush','victim_moving_static',
				'noTouch','victim_moving_moving','victim_moving_static',
				'victim_static_moving','victim_static_static','harm_moving_moving',
				'harm_moving_static','harm_static_moving','harm_static_static','sim1Patient',
				'sim1Fireball','sim2Patient','sim2Fireball','sim3Patient',
				'sim3Fireball','sim4Patient','sim4Fireball']
	
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
	
	impulses = map(lambda x: x/max(impulses)*100, impulses)
	data = parseSQL().values()[:28]
	data = normalize(np.array(data))
	realData = []
	for i in range(len(data)):
		for j in range(len(data[i])):
			realData.append(data[i][j])
	# data = map(lambda x: sum(x)/len(x), data)

	# get rid of 0s for log functions
	# for item in impulses:
	# 	if item == 0:
	# 		impulses[impulses.index(item)] = 1
	predictor = np.array(impulses)
	for i in range(len(data)):
		myFormattedList = [ '%.2f' % elem for elem in data[i] ]
		print i,": ", myFormattedList
		print ""
		response = np.array(data[i])
		plt.plot(predictor,response,'ro', label='data')
	

	# # print regression
	# print(stats.linregress(predictor,response))
	# slope, intercept, r_value, p_value, std_err = stats.linregress(predictor,response)
	# # plot regression
	# plt.plot(predictor,response,'ro', label='data')
	# plt.plot(predictor, intercept + slope*predictor, 'blue', label='fitted line')
	# plt.legend()
	plt.show()
	
	# create bar graph of total impulses per simulation
	# plt.bar(idx,impulses)
	# for xe, ye in zip(idx, data):
	# 	plt.plot(xe, ye, 'ro')
	# plt.plot()
	# plt.xticks(idx, sims, rotation=50)
	# plt.ylabel('Total Impulses')
	# plt.title('Effort Comparison for Sims')
	# plt.tight_layout()
	# plt.savefig('total_impulses.png')
	# plt.show()

def compareKinematics():
	'''
	Plots two bar plots. One for Moral Kinematics data and one for
	Moral Dynamics data.
	'''
	# impulses
	impulses = []

	# agreements for each comparison in Moral Kinematics
	kinematics = [0.82, 0.75, 0.75, 1.0, 
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
		idx = range(1, 12)
		xLabels = ['1. LongDist v ShortDist', '3. Moving v Static', '7. FastColl v SlowColl', '8. Dodge v NoTouch',
				   '9. Dodge v Static', '10. Static v NoTouch', '11. Moving v Dodge', 
				   '12. LongPush v DoublePush', '13. MedPush v MedDist', '14. LongPush v MedPush',
				   '15. LongPush v LongDist']

		# double bar plot
		plt.subplot(111)
		plt.ylabel("Agreement")
		plt.title("Moral Kinematics (Empirical) vs Moral Dynamics Predictions")
		# Moral Kinematics data
		plt.bar(idx, kinematics, width=0.4, color='b', label='Empirical')
		# Moral Dynamics data - need to plot bars next to Kinematics bars
		plt.bar(map(lambda x:x+0.4, idx), dynamics, width=0.4, color='r', label='Dynamics')
		plt.xticks(idx, xLabels, rotation='70')
		plt.legend(loc="best")
		plt.plot(range(1,12),[0.5]*11, "k--")
		plt.tight_layout()
		#plt.savefig('kinematics_dynamics_comparison.png')
		plt.show()

def compareModel():
	'''
	Plots two bar plots. One for Moral Kinematics data and one for
	Moral Dynamics data.
	'''
	# impulses
	impulses = []

	data = parseSQL().values()
	data = map(lambda x: sum(x)/len(x)+0.0, data)
	kinematics = calcProb(data)

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
		plt.title("Empirical Data (Blue) vs Model Predictions (Red)")
		# Moral Kinematics data
		plt.bar(idx, kinematics, width=0.2, color='b', label='Kin')
		# Moral Dynamics data - need to plot bars next to Kinematics bars
		plt.bar(map(lambda x:x+0.2, idx), dynamics, width=0.2, color='r', label='Dyn')
		plt.xticks(idx, xLabels, rotation='70')
		#plt.legend(loc="best")
		plt.plot([0.5]*17, "k--")
		plt.tight_layout()
		plt.savefig('model_data_comparison.png')
		plt.show()

def calcProb(a):
	'''
	Calculate probability one simulation would be deemed worse than another
	using Luce's Choice Theorem. Currently calculates probabilities of the
	same situations presented in Moral Kinematics by Iliev et. al, 2012.
	'''
	prob = []

	# longDistancev1 vs shortDistancev1
	prob.append(a[2]/(a[0]+a[2]))
	# longDistancev2 vs mediumDistancev2
	#prob.append(0)
	# victim_moving_static "Moving" vs static
	prob.append(a[14]/(a[3]+a[14]))
	# medium push vs downhill
	#prob.append(0)
	# uphill vs downhill
	#prob.append(0)
	# uphill vs medium push
	#prob.append(0)
	# fastCollision vs slowCollision
	prob.append(a[5]/(a[5]+a[4]))
	# dodge vs noTouch
	prob.append(a[6]/(a[6]+a[11]))
	# dodge vs static
	prob.append(a[6]/(a[3]+a[6]))
	# static vs noTouch
	prob.append(a[3]/(a[3]+a[11]))
	# victim_moving_static "Moving" vs dodge
	prob.append(a[10]/(a[10]+a[6]))
	# longPush vs doublePush
	prob.append(a[7]/(a[9]+a[7]))
	# Medium Push vs Medium Distance v2
	prob.append(a[8]/(a[8]+a[1]))
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

def parseSQL():
	# begin SQL connection and set cursor
	conn = sqlite3.connect('participants.db')
	cursor = conn.cursor()

	# declare list and dictionary of data from SQL db
	dataList = []
	dataDict = {}

	# traverse SQL database and grab the data
	for row in cursor.execute("SELECT * FROM moral_dynamics WHERE datastring!='NULL'"):
		# begin string
		string = row[16]

		# find data begin in string and extract rest of string
		index = string.index('"data"')
		newString = string[index:]

		# split the string by commas
		for str in newString.split(','):

			# if "clip" or "rating", extract and add to list
			if "clip" in str:
				dataList.append(str[26:-1]) # clean extraction
			if "rating" in str:
				str2 = str[9:-2] # clean extraction
				if "}" in str2:
					str = str2[:-1]
				else:
					str = str2
				dataList.append(str)

	# add the datapoints to dictionary
	print "Data List Length:", len(dataList)
	for i in range(len(dataList)):
		# print dataList[i]
		if i%2 == 0:
			dataDict.setdefault(int(dataList[i]),[]).append(int(dataList[i+1]))
			
	return dataDict

def normalize(input_matrix=np.array(parseSQL().values())):
	# trying to fix data TODO
	matrix = []
	for i in range(len(simulations)):
		matrix.append([])
	for i in range(len(input_matrix)):
		matrix[i] = input_matrix[i][:28]

	# transpose the matrix of participant x responses to get
	# responses x participant
	transposed_matrix = np.array(matrix)#.transpose()

	# find the standard deviation of the transposed_matrix
	std_dev = np.std(transposed_matrix, axis=0)

	# collect row vector of response averages across participants
	average_vector = []
	for response in transposed_matrix:
		average_vector.append(sum(response)/(len(response)+0.0))

	# create z-score matrix of equal length to input_matrix
	z_score_matrix = []
	for i in range(len(simulations)):
		z_score_matrix.append([])
	print z_score_matrix

	for participant in range(len(matrix)):
		for response in range(len(matrix[participant])):
			z_score_matrix[participant].append(
			(matrix[participant][response] - average_vector[participant])/std_dev[participant])
	print "Averages Per Response: ", average_vector
	print "Standard Deviation: ", std_dev
	return z_score_matrix