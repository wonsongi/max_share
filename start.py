import pygame
from pygame.locals import *

# Directions
UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3
JUMP = 4
NO_INPUT = -1
MAX_SPEEDX = 4
MAX_SPEEDY = 7
SCROLL_BORDER = 150

class Game:

    clock = pygame.time.Clock()
 
    def __init__(self):
        self.displaySurf = pygame.display.set_mode((800, 800), pygame.HWSURFACE)
        self.playerSurf = pygame.image.load("images\\player.png").convert()
        transColor = self.playerSurf.get_at((0,0))
        self.playerSurf.set_colorkey(transColor)
        self.playerRect = self.playerSurf.get_rect()
        self.playerRect = self.playerSurf.get_rect()
        self.playerRect.x = 400
        self.playerRect.y = 400
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.jumpDelay = 0
        self.BGSurf = pygame.image.load("images\\background.png").convert()
        self.BGRect = self.BGSurf.get_rect()
        self.BGShift = 400
 
    def init(self):
        pass
           
    def move(self, input, jump):

        #Y
        if self.jumpDelay > 0: self.jumpDelay -= 1
        elif jump:
            self.speed_y = -4
            self.jumpDelay = 60
        self.speed_y += 0.1

        self.playerRect.y += self.speed_y

        if self.playerRect.y < 0:
            self.playerRect.y = 0
            self.speed_y = 0
        if self.playerRect.y >= self.displaySurf.get_height() - 30:
            self.playerRect.y = self.displaySurf.get_height() - 30
            if self.speed_y > 4 : self.speed_y *= -0.6
            else: self.speed_y = 0

        if abs(self.speed_y) > MAX_SPEEDY: self.speed_y = MAX_SPEEDY*MAX_SPEEDY/self.speed_y
        
        #X
        if input == LEFT: self.speed_x -= 0.2
        elif input == RIGHT: self.speed_x += 0.2
        elif self.speed_x !=0: self.speed_x -= 0.05 * abs(self.speed_x)/self.speed_x
 
        if abs(self.speed_x) > MAX_SPEEDX: self.speed_x = MAX_SPEEDX*MAX_SPEEDX/self.speed_x
        if abs(self.speed_x) < 0.1: self.speed_x = 0

        self.playerRect.x += self.speed_x

        realX = self.BGShift + self.playerRect.x
        if self.playerRect.x < SCROLL_BORDER:
            self.playerRect.x = min(realX, SCROLL_BORDER)
            self.BGShift = realX - self.playerRect.x
        elif self.playerRect.x > self.displaySurf.get_width() - SCROLL_BORDER - 30:
            self.BGShift = min(realX - self.displaySurf.get_width() + SCROLL_BORDER + 30, self.BGRect.width -  self.displaySurf.get_width() - SCROLL_BORDER - 30)
            self.playerRect.x = realX - self.BGShift

        if self.playerRect.x < 0:
            self.playerRect.x = 0
            self.speed_x = -self.speed_x
        if self.playerRect.x >= self.displaySurf.get_width() - 30:
            self.playerRect.x = self.displaySurf.get_width() - 30
            self.speed_x = -self.speed_x

    def interaction(self):
        transColor = self.BGSurf.get_at((self.BGShift + self.playerRect.x, self.playerRect.y))
        if transColor == pygame.Color('WHITE'):
            self.speed_y = -self.speed_y
            
    def draw(self):
        self.displaySurf.fill((0,0,0))
        self.displaySurf.blit(self.BGSurf, (-self.BGShift,0))
        self.displaySurf.blit(self.playerSurf, self.playerRect)
        pygame.display.flip()

    def onExecute(self):
        
         while True:
            self.clock.tick(60)
            pygame.event.pump()
            keys = pygame.key.get_pressed()
    # Quit for a player
            if (keys[K_ESCAPE]):
                break
            playerJump = False
            playerInput = NO_INPUT
            if   (keys[K_RIGHT]): playerInput = RIGHT
            elif (keys[K_LEFT]): playerInput = LEFT
            elif (keys[K_UP]): playerInput = UP
            if (keys[K_SPACE]): playerJump = True

    # Main activities: Move characters, calculate interactions, draw the screen
            self.move(playerInput, playerJump)
            self.interaction()
            self.draw()
                    
if __name__ == "__main__" :
    theApp = Game()
    theApp.onExecute()
    pygame.quit()
