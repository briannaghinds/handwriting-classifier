# https://www.youtube.com/watch?v=G8MYGDf_9ho&ab_channel=CodingWithRuss

import pygame

class Button():
    def __init__(self, x, y, image, scale=1):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, screen):
        action = False
        # get the mouse position
        pos = pygame.mouse.get_pos()

        # check if the mouse hovers over the button and if clicks button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button onto screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action