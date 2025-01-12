import math
import pygame
from copy import deepcopy

class Apple:
    def __init__(self,x,y,player):
        self.x = x
        self.y = y
        self.velocityX = 0
        self.velocityY = 0
        self.height = 20
        self.speed = 10
        self.GetDirection(player)
        self.damaged = False
        self.image = pygame.image.load('assets/apple.png')
        self.image = pygame.transform.scale(self.image, (60, 60))


    def GetDirection(self,player):
        '''Init velocity of the apple in the direction of the player'''
        playerCopy = player
        dirX = playerCopy.x - self.x - 15
        dirY = playerCopy.y - self.y 
        norm = math.sqrt(dirX**2+dirY**2)
        norm_dirX = dirX/norm
        norm_dirY = dirY/norm
        self.velocityX = norm_dirX*self.speed
        self.velocityY = norm_dirY*self.speed


    def update(self,screen):
        self.Move()
        self.Draw(screen)

    def Move(self):
        self.x += self.velocityX
        self.y += self.velocityY
        
    def IsOut(self):
        '''if the apple is out of the screen'''
        if(self.x < -20 or self.x> 1600 or self.y < -40 or self.y > 1600):
            return True
        return False
    
    def Draw(self,screen):
        screen.blit(self.image,  (self.x,self.y))
