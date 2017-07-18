import pymunk
import pygame
import agents
import handlers
import math
import pymunk.pygame_util
from pygame.locals import *
import glob
import helper

class simulation:

	def __init__(self, simVector):
		pygame.init()
		self.space = pymunk.Space()
		self.screen = screen = pygame.display.set_mode((1000,600))
		self.drawOptions = pymunk.pygame_util.DrawOptions(screen)
		self.clock = pygame.time.Clock()	
		self.collisionHandlers = simVector[0]

		self.xImpsAgent = []
		self.yImpsAgent = []
		self.xImpsPatient = []
		self.yImpsPatient = []
		self.xImpsFireball = []
		self.yImpsFireball = []
		self.total = []
		self.running = True
		self. tick = 0

		self.agent = simVector[1][0]
		self.space.add(agent.body, agent.shape)
		self.patient = simeVector[1][1]
		self.space.add(patient.body, patient.shape)
		self.fireball = simVector[1][2]
		self.space.add(fireball.body, fireball.shape)

	def patientAnimation():
		pass

	def quit():
		pygame.quit()
		pygame.display.quit()

	def runSimulation():
		pass

	def 

