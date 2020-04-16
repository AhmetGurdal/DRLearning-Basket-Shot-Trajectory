import pygame, sys
from math import atan, radians, cos, sin
import time
import random

BLACK = (0, 0, 0)

Blue    = (20,20,100)
Buff    = (100,180,180)

class PowerBar:
    def __init__(self):
        self.running = True

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (320, 100, 640, 100), 1)
        pygame.draw.rect(screen, BLUE, (320, 100, self.power * 640 / 100, 100), 0)

    def get_angle(self):
        #x, y = pygame.mouse.get_pos()
        #dx = x - world.ball.state[0]
        #dy = 640 - y - world.ball.state[1]
        #if dx == 0:
        #    angle = radians(90)
        #else:
        #    angle = atan(dy / float(dx))
        #    if angle < 0:
        #        angle = 0
        #    elif angle > 90:
        #        angle = radians(90)
        time.sleep(0.1)
        angle = random.randrange(1,45) / 30.0
        #print("Angle: " + str(angle))
        return angle
        #return angle

    def start(self, world,agent):
        event = pygame.event.poll()
        self.shoot_balls(world,agent)


    def shoot_ball(self,world,ball,agent):
       
        #print(world.shot_from)
        angle,vel = agent.createNextAction(world.shot_from - 100)
        print("WorldSHOT:" + str(world.shot_from))
        ball.agent_State[0] = world.shot_from - 100
        ball.agent_State[1] = angle
        ball.agent_State[2] = vel
        angle = angle / 30.0
        vel_x = vel * cos(angle)
        vel_y = vel * sin(angle)
        ball.set_vel([vel_x,vel_y])

    def shoot_balls(self, world,agent):
        for i in range(world.numberOfBalls):
            world.shot = True
            print("ShotFrom:")
            print(world.shot_from)
            #world.shot_from = world.balls[i].state[0]
            angle,vel = agent.createNextAction(world.shot_from)
            world.balls[i].agent_State[0] = world.shot_from
            world.balls[i].agent_State[1] = angle
            world.balls[i].agent_State[2] = vel
            #print("Angle : " + str(angle))
            
            
            #vel = 150 * self.power / 100
            #vel = random.randint(110,130)
            #print("Vel: " + str(vel))
            angle = angle / 30.0
            vel_x = vel * cos(angle)
            vel_y = vel * sin(angle)
            world.balls[i].set_vel([vel_x, vel_y])
        # testing value, 100% will score at default position
        # world.ball.set_vel([75, 96])

