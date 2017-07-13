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
	print("-----AVAILABLE EXPERIMENT 1 SIMS-----")
	print("1. Short Distance v1")
	print("2. Medium Distance v2")
	print("3. Long Distance v1")
	print("4. Long Distance v2")
	print("5. Static")
	print("6. Slow Collision")
	print("7. Fast Collision")
	print("8. Dodge")
	print("9. Double Push")
	print("10. Medium Push")
	print("11. Long Push")
	print("12. Moving")
	print("13. No Touch")
	print("-----AVAILABLE EXPERIMENT 2 SIMS-----")
	print("14. Victim Moving Moving")
	print("15. Victim Moving Static")
	print("16. Victim Static Moving")
	print("17. Victim Static Static")
	print("18. Harm Moving Moving")
	print("19. Harm Moving Static")
	print("20. Harm Static Moving")
	print("21. Harm Static Static")
	print("-----EXTRA MORAL DYNAMICS SIMS-------")
	print("22. Sim 1 Patient")
	print("23. Sim 1 Fireball")
	print("24. Sim 2 Patient")
	print("25. Sim 2 Fireball")
	print("26. Sim 3 Patient")
	print("27. Sim 3 Fireball")
	print("28. Sim 4 Patient")
	print("29. Sim 4 Fireball")
	print("-----MTURK INTRO SIMS----------------")
	print("30. Agent Runs to Fireball")
	print("31. Patient Walks to Fireball")
	print("32. Fireball Moving")
	print("33. Agent Saves Patient")
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

	time=200
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

def snapshot(screen, counter):
	pygame.image.save(screen, "image"+str(counter)+".png")