import pygame

class Player:
    def __init__(self):
        self.x = 100
        self.y = 200
        self.velocityv = 300
        self.gravity = 0
    def Move(self,keys,dt):
        
        if keys[pygame.K_a]:
            self.x -= 300 * dt
        if keys[pygame.K_d]:
            self.x += 300 * dt
