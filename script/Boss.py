import pygame

class Boss:
    def __init__(self):
        self.x = 400                
        self.y = 200                   
        self.max_life = 10      
        self.life = self.max_life         
        self.speed = 300            
        self.width = 50              
        self.height = 50
        self.is_colliding = False              

    def update(self, player):
        self.check_collision(player)
        self.display(player.screen)

    def check_collision(self, player):
        boss_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        player_rect = pygame.Rect(player.x - player.height // 2, player.y - player.height // 2, player.height, player.height)
        
        if boss_rect.colliderect(player_rect):
            if self.is_colliding == False :
                print("touché")
                self.take_damage(1)
                self.is_colliding = True
        else :
            self.is_colliding = False


    def take_damage(self, amount):
        self.life -= amount
        if self.life < 0:
            self.life = 0

    def display(self, screen):
        boss_color = (255, 0, 0)
        pygame.draw.rect(screen, boss_color, (self.x, self.y, self.width, self.height))
        
        life_bar_width = 500
        life_ratio = self.life / self.max_life
        pygame.draw.rect(screen, (0, 0, 0), (10, 10, life_bar_width, 25)) 
        pygame.draw.rect(screen, (0, 255, 0), (10, 10, life_bar_width * life_ratio, 25))  

