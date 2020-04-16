import pygame

BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Text:
    def text_objects(self, text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def score_display(self, world, screen):
        p1color = RED
        
        self.add_to_screen(screen, 30, "Player 1: " + str(world.p1score) + " points", 150, 50, p1color)



    def add_to_screen(self, screen, font_size, text, center_x, center_y, color):
        largeText = pygame.font.Font('freesansbold.ttf', font_size)
        TextSurf, TextRect = self.text_objects(text, largeText, color)
        TextRect.center = (center_x, center_y)
        screen.blit(TextSurf, TextRect)
