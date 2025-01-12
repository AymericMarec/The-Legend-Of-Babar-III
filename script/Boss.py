import pygame
import random
from script.Apple import Apple
class Boss:
    def __init__(self):
        self.x = -400                
        self.y = 100                   
        self.max_life = 5      
        self.life = self.max_life         
        self.speed = 800            
        self.width = 100              
        self.height = 400
        self.is_colliding = False
        self.velocityX = 0
        self.velocityY = 0
        self.attack_cooldown = 5
        self.throwing_apple = 0
        self.Apple = []
        # Charger l'image du boss
        self.original_image = pygame.image.load("./Assets/snake.png")
        self.original_image = pygame.transform.scale(self.original_image, (self.width, self.height))  # Ajuste la taille si nécessaire
        self.image = self.original_image  # Image actuelle affichée
        self.hitbox = pygame.Rect(self.x, self.y + 10, self.width, self.height)


    def update(self, player, screen, dt):
        self.attack(dt, player)
        self.display(screen)
        self.move(dt,player)
        self.MoveApple(screen)

    def update_hitbox(self, direction) :
        if direction == "HORIZON" :
            self.hitbox = pygame.Rect(self.x, self.y + 10, 400, 100)
        else : 
            self.hitbox = pygame.Rect(self.x, self.y + 10, 100, 400)

    def move(self,dt,player):
        self.x += self.velocityX * dt
        self.y += self.velocityY * dt
        self.change_orientation() 

        if self.throwing_apple > 0:
            dtmax = int(dt * 1000)
            chance_to_throw = 45
            if(random.randint(0,dtmax*chance_to_throw) < dtmax):
                self.throwing_apple-=1
                apple = Apple(self.x,self.y,player)
                self.Apple.append(apple)

    def change_orientation(self):
        if self.velocityX > 0: 
            self.image = pygame.transform.rotate(self.original_image, -90)
            self.update_hitbox("HORIZON")
        elif self.velocityX < 0: 
            self.image = pygame.transform.rotate(self.original_image, 90)
            self.update_hitbox("HORIZON")
        elif self.velocityY > 0: 
            self.image = pygame.transform.rotate(self.original_image, 180)
            self.update_hitbox("VERTICAL")
        elif self.velocityY < 0:  
            self.image = pygame.transform.rotate(self.original_image, 0)
            self.update_hitbox("VERTICAL")

    def attack(self, dt, player):
        if self.attack_cooldown < 0:
            self.throwing_apple = 0
            self.velocityX = 0
            self.velocityY = 0
            if random.randint(1, 2) == 1:
                self.MovingAttack(player)
            else:
                self.ThrowApple(player)
            self.attack_cooldown = 5
        else:
            self.attack_cooldown -= dt

    def MovingAttack(self, player):
        self.speed = 800
        if random.randint(1, 2) == 1:
            self.y = player.y + 40
            self.HorizontalMovement()
        else:
            self.x = player.x - 15
            self.VerticalMovement()

    def ThrowApple(self, player):
        self.speed = 500
        self.throwing_apple = 3
        if random.randint(1, 2) == 1:
            self.y = 20
            self.HorizontalMovement()
        else:
            self.x = 20
            self.VerticalMovement()

    def HorizontalMovement(self):
        tempwidth = self.width
        self.width = self.height
        self.height = tempwidth
        if random.randint(1, 2) == 1:
            self.x = -400
            self.velocityX = self.speed
        else:
            self.x = 1400
            self.velocityX = -self.speed

    def VerticalMovement(self):
        if random.randint(1, 2) == 1:
            self.y = -400
            self.velocityY = self.speed
        else:
            self.y = 1400
            self.velocityY = -self.speed

    def take_damage(self, amount):
        self.life -= amount
        if self.life < 0:
            self.life = 0

    def display(self, screen):
        # Afficher l'image du boss
        screen.blit(self.image, (self.x, self.y))
        
        # Barre de vie
        life_bar_width = screen.get_width() * 0.7
        margin = (screen.get_width() - life_bar_width) / 2
        life_ratio = self.life / self.max_life
        pygame.draw.rect(screen, (0, 0, 0), (margin, screen.get_height() - 45, life_bar_width, 25), border_radius=10) 
        pygame.draw.rect(screen, (139, 0, 0), (margin, screen.get_height() - 45, life_bar_width * life_ratio, 25), border_radius=10)


    def MoveApple(self,screen):
        for apple in self.Apple:
            apple.update(screen)
            if(apple.IsOut() or apple.damaged == True):
                self.Apple.remove(apple)
