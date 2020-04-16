import pygame
from Ball import Ball2D
from World import World
from PowerBar import PowerBar
from Text import Text
from Agent import Agent

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

def main():

   
    pygame.init()

    clock = pygame.time.Clock()

    
    win_width = 1280
    win_height = 640

    screen = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption('Basketball')

    world = World()
    power = PowerBar()
    scoreboard = Text()
    agent = Agent(150,45,900)
    
    
    world.add_rim('disk-red.png', 5).set_pos([1000, 300])
    world.add_rim('disk-red.png', 5).set_pos([1075, 300])
    world.shot_from = 100
    dt = 0.1
    while(True):
        clock.tick(60)
        screen.fill(WHITE)
        #power.draw(screen)
        world.draw(screen)
        pygame.draw.arc(screen, RED, (50,50,50,50), 1, 1, 10)
        pygame.draw.line(screen, RED, [1000, 340], [1075, 340], 10)
       
        pygame.draw.line(screen, RED, [1075, 250], [1075, 640], 10)
        scoreboard.score_display(world, screen)
        
        if not world.shot:
            world.start(power, agent)
        else:
            won = world.update(dt, power, agent)  ### change position here
            

        pygame.display.update()

if __name__ == '__main__':
    main()
