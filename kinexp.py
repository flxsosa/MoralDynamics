'''
Script for recreating Moral Kinematics experiments.

Felix Sosa
March 10, 2017
'''

import pymunk
import pygame
from pygame.locals import *
import sys, random
import pymunk.pygame_util

def to_pygame(p):
    return int(p.x), int(-p.y+600)

def add_ball(space):
    mass = 1
    radius = 14
    moment = pymunk.moment_for_circle(mass, 0, radius) # 1
    body = pymunk.Body(mass, moment)
    x = random.randint(120,380)
    body.position = x, 550 # 3
    shape = pymunk.Circle(body, radius)
    space.add(body,shape) # 5
    return shape

def add_Static_L(space):
    pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = (300,300)
    l1 = pymunk.Segment(body, (-150,0), (255,0), 5)
    l2 = pymunk.Segment(body, (-150,0), (-150, 50), 5)

    space.add(l1,l2)
    return l1,l2

def main():
    pygame.init()
    screen = pygame.display.set_mode((600,600))
    pygame.display.set_caption("Joints. Just wait and the L will tip over")
    clock = pygame.time.Clock()

    space = pymunk.Space() # 2
    space.gravity = (0.0, -900.0)

    LINES = add_Static_L(space)
    balls = []
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    ticks_to_next_ball = 10
    while True:
     event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)
        
        ticks_to_next_ball -= 1
        if ticks_to_next_ball <=0:
            ticks_to_next_ball = 25
            ball_shape = add_ball(space)
            balls.append(ball_shape)

        space.step(1/50.0) # 3
    
        screen.fill((255,255,255))
        space.debug_draw(draw_options)

        pygame.display.flip()
        clock.tick(50)

if __name__== '__main__':
    sys.exit(main())