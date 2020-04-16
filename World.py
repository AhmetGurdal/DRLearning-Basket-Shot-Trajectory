import pygame
import numpy as np
from Ball import Ball2D
import sys
from Rim import Rim2D
import time

class World:

   
    
    def __init__(self):
        
        self.rim = []
        self.balls = list()
        self.e = 1. # Coefficient of restitution
        self.shot = False
        self.p1score = 0
        self.p1turn = True
        self.count = 0
        self.numberOfBalls= 6
        self.shot_from = 0

    
    def add_ball(self, imgfile, radius, mass=1.0):
        for i in range(self.numberOfBalls):
            disk = Ball2D(imgfile, radius, mass)
            self.balls.append(disk)
        

    def update_from(self):
        self.add_ball('disk-blue.png', 15, 0.1)
    

    def reset(self, power):

        self.shot = False
        # default position is 30, 30
        #shot_from = 100 # change position here
        self.ball = self.ball.set_pos([self.shot_from,30])
        self.count += 1

    def update_score(self):
        # score is proportional to distance to the rim, greater distance -> greater score awarded
        score = 10
        if self.p1turn:
            self.p1score += score
        

    def add_rim(self, imgfile, radius):
        rim = Rim2D(imgfile, radius)
        self.rim.append(rim)
        return rim

    def draw(self, screen):
        self.update_from()
        for i in range(self.numberOfBalls):
            self.balls[i].draw(screen)
            for rim in self.rim:
                rim.draw(screen)


    def resetAgain(self,power,agent):
        if(self.shot_from > 900):
            agent.printMatrix("EndOfTrainingData.txt")
            pygame.quit()
            sys.exit(0)


        for i in range(self.numberOfBalls):
            if(self.balls[i].reset):
                self.balls[i].t = 0
                self.balls[i].outer_xy = list()
                self.balls[i].inner_xy = list()
                if(self.p1score == 2000):  #Limit for each positions
                    self.p1score = 0
                    self.shot_from += 1 #Update Shot_From
                if(self.balls[i].scored):
                    agent.addState(self.balls[i].agent_State,6) # state, reward
                    self.update_score()
                    self.balls[i].scored = False
                else:
                    agent.addState(self.balls[i].agent_State,0)
                self.balls[i].reset = False
                power.shoot_ball(self,self.balls[i],agent)
        self.count+=1


    def start(self,power, agent):
        
        event = pygame.event.poll()
        power.shoot_balls(self,agent)

    
    def update(self, dt, power,agent):
        for i in range(self.numberOfBalls):
            self.ball = self.balls[i]
            self.check_for_collision()
            self.ball.update(dt,agent)
            # ball is out of bounds -> reset
            if self.ball.state[0] > 1280 + self.ball.radius or self.ball.state[1] < 0 - self.ball.radius:
                #self.reset(power)
                self.ball.set_pos([self.shot_from,30])
                self.ball.reset = True
                self.resetAgain(power, agent)
                #print("Ball is out")
            # ball is in the rim -> scored
            top_of_ball = self.ball.state[1] + self.ball.radius
            #if(self.ball.state[0] > 1000 and self.ball.state[0] < 1075 and top_of_ball > 305 and top_of_ball < 490):
            #    print("2")

            # (x - 1075) ^ 2 - (y - 300) ^ 2 = 5625
             
            if(top_of_ball >= 270 and top_of_ball <= 375):
                if(self.ball.state[0] >= 1000 and self.ball.state[0] <= 1110):
                    res = (self.ball.state[0]- 1075) ** 2  - (top_of_ball - 300) ** 2
                    if(res <= 10000 and res >= 4900):
                        self.ball.outer_xy = self.ball.state[:2]
                    elif(res < 4900):
                        self.ball.inner_xy = self.ball.state[:2]

                #if(len(self.ball.outer_xy) == 2 and len(self.ball.inner_xy) == 2):
                #    print("Inner : " + str(self.ball.inner_xy))
                #    print("Outer : " + str(self.ball.outer_xy))
                    
            
            if(top_of_ball > 295 and top_of_ball < 305):
                if(self.ball.state[0] > 1000 and self.ball.state[0] < 1075):
                    self.ball.scored = True
                   
                #elif(self.ball.state[0] > 980 and self.ball.state[0] <= 1000):
                    #print("1")
                #elif(self.ball.state[0] > 1075 and self.ball.state[0] <= 1095):
                    #print("2")
            
    def normalize(self, v):
        return v / np.linalg.norm(v)

    def check_for_collision(self):
        if self.check_backboard_collision():
            return

        self.check_rim_collision()        

    def check_backboard_collision(self):
        right_of_ball = self.ball.state[0] + self.ball.radius
        if right_of_ball >= 1075 and right_of_ball <= 1090:
            bottom_of_ball = self.ball.state[1] - self.ball.radius
            # hit top of backboard
            if bottom_of_ball > 390 and bottom_of_ball <= 395:
                self.ball.state = self.ball.prev_state
                self.ball.set_vel([self.ball.state[2], -self.ball.state[3]])
                return True
            # hit side of backboard
            if bottom_of_ball > 0 and bottom_of_ball <= 390:
                self.ball.state = self.ball.prev_state
                self.ball.set_vel([-self.ball.state[2], self.ball.state[3]])
                return True
        return False

    def check_rim_collision(self):
        pos_i = self.ball.state[0:2]
        for j in range(0, len(self.rim)):
            
            pos_j = np.array(self.rim[j].state[0:2])
            dist_ij = np.sqrt(np.sum((pos_i - pos_j)**2))

            radius_j = self.rim[j].radius
            if dist_ij > self.ball.radius + radius_j:
                continue

            self.ball.state = self.ball.prev_state

            vel_i = np.array(self.ball.state[2:])
            n_ij = self.normalize(pos_i - pos_j)

            mass_i = self.ball.mass

            J = -(1+self.e) * np.dot(vel_i, n_ij) / ((1./mass_i + 1.))
            vel_i_aftercollision = vel_i + n_ij * J / mass_i

            self.ball.set_vel(vel_i_aftercollision)
            return
