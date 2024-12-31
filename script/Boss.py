import pygame
import random

class Boss:
    def __init__(self):
        self.x = 400                
        self.y = 200                   
        self.max_life = 10      
        self.life = self.max_life         
        self.speed = 800            
        self.width = 50              
        self.height = 50
        self.is_colliding = False
        self.body = None              
        self.velocityX = 0
        self.velocityY = 0
        self.attack_cooldown = 0
        self.throwing_apple = 0


    def update(self,player, screen,dt):
        self.attack(dt,player)
        self.display(screen)
        self.move(dt)

    def move(self,dt):
        self.x += self.velocityX * dt
        self.y += self.velocityY * dt
        if(self.throwing_apple > 0):
            dtmax = int(dt*1000)
            chance_to_throw = 45
            if(random.randint(0,dtmax*chance_to_throw) < dtmax):
                self.throwing_apple-=1
                #send apple
                print("attaaaack")


    def attack(self,dt,player):
        if self.attack_cooldown < 0 :
            self.throwing_apple = 0
            self.velocityX = 0
            self.velocityY = 0
            if(random.randint(1,2) == 1):
                self.MovingAttack(player)
            else:
                self.ThrowApple(player)
            self.attack_cooldown = 5
        else :
            self.attack_cooldown -= dt
    def MovingAttack(self,player):
        self.speed = 800
        if(random.randint(1,2) == 1):
            self.y = player.y -40
            self.HorizontalMovement()
        else:
            self.x = player.x
            self.VerticalMovement()

    def ThrowApple(self,player):
        self.speed = 500
        self.throwing_apple = 3
        if(random.randint(1,2) == 1):
            self.y = 20
            self.HorizontalMovement()
        else:
            self.x = 20
            self.VerticalMovement()

    def HorizontalMovement(self):
        if(random.randint(1,2) == 1):
            self.x = -100
            self.velocityX = self.speed
        else:
            self.x = 1400
            self.velocityX = -self.speed
            
    def VerticalMovement(self):
        if(random.randint(1,2) == 1):
            self.y = -100
            self.velocityY = self.speed
        else:
            self.y = 1400
            self.velocityY = -self.speed


    def take_damage(self, amount):
        self.life -= amount
        if self.life < 0:
            self.life = 0

    def display(self, screen):
        boss_color = (255, 0, 0)
        self.body = pygame.draw.rect(screen, boss_color, (self.x, self.y, self.width, self.height))
        
        life_bar_width = screen.get_width() * 0.8
        margin =  (screen.get_width() - (screen.get_width() * 0.8))/2
        life_ratio = self.life / self.max_life
        pygame.draw.rect(screen, (0, 0, 0), (margin, 20, life_bar_width, 25)) 
        pygame.draw.rect(screen, (0, 255, 0), (margin, 20, life_bar_width * life_ratio, 25))  

    # def check_collision(self, player):
    #     boss_rect = pygame.Rect(self.x, self.y, self.width, self.height)
    #     player_rect = pygame.Rect(player.x - player.height // 2, player.y - player.height // 2, player.height, player.height)
        
    #     if boss_rect.colliderect(player_rect):
    #         if self.is_colliding == False :
    #             print("touché")
    #             self.take_damage(1)
    #             self.is_colliding = True
    #     else :
    #         self.is_colliding = False
