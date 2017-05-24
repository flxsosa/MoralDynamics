'''
Main file for Moral Dynamics

March 31, 2017
Felix Sosa
'''

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

def main():
	'''
	Entry point
	'''
	print("=================================================")
	print("1. Show Simulations")
	print("2. Run Guesses")
	print("3. Plot Sims")
	print("0. EXIT")
	print("=================================================")
	print("Please choose an option or [0] to exit:")
	choice = raw_input()

	# display simulation options
	if choice == '1':
		print("=================================================")
		print("1. Short Distance")
		print("2. Medium Distance")
		print("3. Long Distance")
		print("4. Static")
		print("5. Uphill [N/A]")
		print("6. Downhill [N/A]")
		print("7. Slow Collision")
		print("8. Fast Collision")
		print("9. Dodge")
		print("10. Double Touch")
		print("11. Medium Push")
		print("12. Long Push")
		print("13. Touch")
		print("14. Push Fireball")
		print("0. EXIT")
		print("=================================================")
		print("Please choose a Simulation [1-13] or [0] to exit:")
		choice = raw_input()
		
		while (choice != '0'):
			# initialize pygame and create a space to contain the simulation
			pygame.init()
			space = pymunk.Space()

			# create a screen of 600x600 pixels
			screen = pygame.display.set_mode((600,600))	
			drawOptions = pymunk.pygame_util.DrawOptions(screen)

			if (choice == '1'):
				simulations.shortDistance(space, screen, drawOptions)
			elif (choice == '2'):
				simulations.mediumDistance(space, screen, drawOptions)
			elif (choice == '3'):
				simulations.longDistance(space, screen, drawOptions)
			elif (choice == '4'):
				simulations.static(space, screen, drawOptions)
			elif (choice == '5'):
				simulations.uphill(space, screen, drawOptions)
			elif (choice == '6'):
				simulations.downhill(space, screen, drawOptions)
			elif (choice == '7'):
				simulations.slowCollision(space, screen, drawOptions)
			elif (choice == '8'):
				simulations.fastCollision(space, screen, drawOptions)
			elif (choice == '9'):
				simulations.dodge(space, screen, drawOptions)
			elif (choice == '10'):
				simulations.doubleTouch(space, screen, drawOptions)
			elif (choice == '11'):
				simulations.mediumPush(space, screen, drawOptions)
			elif (choice == '12'):
				simulations.longPush(space, screen, drawOptions)
			elif (choice == '13'):
				simulations.touch(space, screen, drawOptions)
			elif (choice == '14'):
				simulations.pushFireball(space, screen, drawOptions)
			else:
				print("Must be an integer [0-14]")
			pygame.quit()
			pygame.display.quit()
			print("Please choose a Simulation [1-14] or [0] to exit:")
			choice = raw_input()
			
		print("Goodbye")
		sys.exit()
		
	# display guess options
	if choice == '2':
		print("=================================================")
		print("1. Short Distance")
		print("2. Medium Distance")
		print("3. Long Distance")
		print("4. Static")
		print("5. Uphill [N/A]")
		print("6. Downhill [N/A]")
		print("7. Slow Collision")
		print("8. Fast Collision")
		print("9. Dodge")
		print("10. Double Touch")
		print("11. Medium Push")
		print("12. Long Push")
		print("13. Touch")
		print("14. Push Fireball")
		print("0. EXIT")
		print("=================================================")
		print("Please choose a Simulation [1-13] or [0] to exit:")
		choice = raw_input()
		
		while (choice != '0'):
			# create a space to contain the simulation
			space = pymunk.Space()

			# each choice executes an enumeration over a fixed interval of guess
			# impulses for each sim
			if (choice == '1'):
				infer.enum(simulations.shortDistance, 100, 300)
			elif (choice == '2'):
				infer.enum(simulations.mediumDistance, 100, 300)
			elif (choice == '3'):
				infer.enum(simulations.longDistance, 100, 300)
			elif (choice == '4'):
				infer.enum(simulations.static, 250, 450)
			elif (choice == '5'):
				simulations.uphill(space, screen, drawOptions)
			elif (choice == '6'):
				simulations.downhill(space, screen, drawOptions)
			elif (choice == '7'):
				infer.enum(simulations.slowCollision, 300, 500)
			elif (choice == '8'):
				infer.enum(simulations.fastCollision, 170, 370)
			elif (choice == '9'):
				infer.enum(simulations.dodge, 50, 250)
			elif (choice == '10'):
				infer.enum(simulations.doubleTouch, 70, 270)
			elif (choice == '11'):
				infer.enum(simulations.mediumPush, 50, 250)
			elif (choice == '12'):
				infer.enum(simulations.longPush, 10, 200)
			elif (choice == '13'):
				infer.enum(simulations.touch, 150, 350)
			elif (choice == '14'):
				infer.enum(simulations.pushFireball, 175, 375)
			else:
				print("Must be an integer [0-14]")
			pygame.quit()
			pygame.display.quit()
			print("Please choose a Simulation [1-14] or [0] to exit:")
			choice = raw_input()
			
		print("Goodbye")
		sys.exit()

	# display comparison options
	if choice =='3':
		print("=================================================")
		print("1. Short Distance")
		print("2. Medium Distance")
		print("3. Long Distance")
		print("4. Static")
		print("5. Uphill [N/A]")
		print("6. Downhill [N/A]")
		print("7. Slow Collision")
		print("8. Fast Collision")
		print("9. Dodge")
		print("10. Double Touch")
		print("11. Medium Push")
		print("12. Long Push")
		print("13. Touch")
		print("14. Push Fireball")
		print("0. EXIT")
		print("=================================================")

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



if __name__ == '__main__':
	sys.exit(main())