'''
Set of helper functions for Moral Dynamics 
modules

Felix Sosa
June 27, 2017
'''
import pygame

# sprites
BACKGROUND_S = pygame.image.load("Sprites/sand.jpg")
BACKGROUND_G = pygame.image.load("Sprites/grass.jpg")
fireSprite = pygame.image.load("Sprites/firea.png")
patientSprite = pygame.image.load("Sprites/Patient.png")
agentSprite = pygame.image.load("Sprites/Agent.png")

def printOptions():
	'''
	Prints simulation options to user.
	'''
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
	print("Please choose a Simulation [1-14] or [0] to exit:")

def setBackground(screen):
	'''
	Sets the background for simulations. Expected screen
	of (1000px,600px).
	'''
	# top grass row
	screen.blit(BACKGROUND_S, (0,0))
	screen.blit(BACKGROUND_S, (200,0))
	screen.blit(BACKGROUND_S, (400,0))
	screen.blit(BACKGROUND_S, (600,0))
	screen.blit(BACKGROUND_S, (800,0))
	# bottom grass row
	screen.blit(BACKGROUND_S, (0,400))
	screen.blit(BACKGROUND_S, (200,400))
	screen.blit(BACKGROUND_S, (400,400))
	screen.blit(BACKGROUND_S, (600,400))
	screen.blit(BACKGROUND_S, (800,400))
	# sand row
	screen.blit(BACKGROUND_S, (0,200))
	screen.blit(BACKGROUND_S, (200,200))
	screen.blit(BACKGROUND_S, (400,200))
	screen.blit(BACKGROUND_S, (600,200))
	screen.blit(BACKGROUND_S, (800,200))

def wait(screen, space, options, cylinder, ball, cone):
	'''
	Creates a pause before any simulation runs if called
	'''
	pBall = (ball.body.position[0]-30,ball.body.position[1]-30)
	pCone = (cone.body.position[0]-30,cone.body.position[1]-30)
	pAgent = (cylinder.body.position[0]-30,cylinder.body.position[1]-30)

	time=100
	while (time > 0):
			time-=1
			# draw screen
			screen.fill((255,255,255))
			space.debug_draw(options)
			setBackground(screen)
			screen.blit(fireSprite, pBall)
			screen.blit(patientSprite, pCone)
			screen.blit(agentSprite, pAgent)
			pygame.display.flip()