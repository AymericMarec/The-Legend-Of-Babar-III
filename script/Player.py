import pygame
import time

class Player:
    def __init__(self):
        self.x = 300        
        self.y = 200   
        self.height = 20

        self.gravity = 30
        self.max_fall_speed = 300    
        self.speed = 300  

        self.velocityX = 0  
        self.velocityY = 0

        self.MaxJump = 2            
        self.jump = self.MaxJump    
        self.jumpForce = 15    

        self.isFacing = "RIGHT"     
        self.dashspeed = 3          
        self.dashing = False
        self.dashingtime = 5
        self.dashcooldown = 0

        self.attackFacing = "RIGHT"
        self.attackX = 0
        self.attackY = 0
        self.Damaged = False
        self.isAttacking = False
        self.attack_cooldown = 0
        self.attack_range = 80
        self.attack_width = 100
        self.attack_timer = 0
        self.attack_duration = 10
        
        self.life = 0
        self.is_colliding = False

    def update(self,keys,dt,screen,Map,button,boss):
        '''Function called every frame in the game'''
        self.Fall(dt,Map)
        self.Move(keys,dt,button)
        self.Collision_Detection(Map)
        self.Attack(screen,boss)
        self.check_collision(boss)
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.x += self.velocityX
        self.y -= self.velocityY
        self.Display(screen)

    def Attack(self,screen,boss):
        if self.isAttacking:
            
            if self.attackFacing == "RIGHT":
                attack_rect = pygame.Rect(
                    self.attackX + self.height // 2,
                    self.attackY - self.attack_width//2 ,
                    self.attack_range,
                    self.attack_width,
                )
            elif self.attackFacing == "LEFT": 
                attack_rect = pygame.Rect(
                    self.attackX - self.attack_range - self.height // 2,
                    self.attackY - self.attack_width // 2,
                    self.attack_range,
                    self.attack_width,
                )
            elif self.attackFacing == "TOP":
                attack_rect = pygame.Rect(
                    self.attackX - self.attack_range + self.height,
                    self.attackY - self.attack_width + self.height // 2,
                    self.attack_width,
                    self.attack_range,
                ) 
            if attack_rect.colliderect(boss.body) and not self.Damaged:
                self.Damaged = True
                boss.take_damage(1)

            pygame.draw.rect(screen, "yellow", attack_rect, 1)

            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.isAttacking = False

    def Move(self, keys, dt, button):  
        '''Gestion of the player Movement'''
        if self.dashing:
            self.Dash(dt)
            self.dashingtime -= 1
            if self.dashingtime <= 0:
                self.dashing = False
                self.dashingtime = 5
            return  # Ne pas traiter les mouvements normaux pendant le dash

        if self.dashcooldown > 0:
            self.dashcooldown -= 1

        if keys[pygame.K_q]:
            # Moving Left
            self.isFacing = "LEFT"
            self.velocityX = -self.speed * dt
        elif keys[pygame.K_d]:
            # Moving Right
            self.isFacing = "RIGHT"
            self.velocityX = self.speed * dt
        else:
            # if the player doesn't press any key, stop movement
            self.velocityX = 0

        if keys[pygame.K_m]:
            # Dashing
            if not self.dashing and self.dashcooldown == 0:
                self.dashing = True
                self.dashcooldown = 15

        if keys[pygame.K_SPACE] and self.jump >= 1 and not self.velocityY > 0:
            if self.jump == self.MaxJump:
                self.velocityY = self.jumpForce
            else:
                # Double / triple jump less efficient
                self.velocityY = self.jumpForce / 1.5
            # Remove 1 player jump
            self.jump -= 1

        if button[0] and self.attack_cooldown <= 0:
            if keys[pygame.K_z]:    # up attack
                self.attackFacing = "TOP"
            else:
                self.attackFacing = self.isFacing
            self.attackX = self.x
            self.attackY = self.y
            self.isAttacking = True
            self.attack_timer = self.attack_duration
            self.attack_cooldown = 30
            self.Damaged = False


    def Dash(self, dt):
        if self.isFacing == "LEFT" :
            self.velocityX -= self.speed * dt * self.dashspeed
        else :
            self.velocityX += self.speed * dt * self.dashspeed
    def Fall(self, dt, Map):
        '''Apply gravity when the player is not on the ground otherwise eh don't fall'''
        if not self.is_collision(Map,self.x,self.y+self.height*1.25):
            self.velocityY -= self.gravity * dt
            
            if self.velocityY < -self.max_fall_speed:
                self.velocityY = -self.max_fall_speed
        else:
            self.velocityY = 0
            self.jump = self.MaxJump
    def Collision_Detection(self,Map):
        '''Stop the player if he cross a plateform , on the side and above him'''
        # check above
        if(self.is_collision(Map,self.x,self.y-self.height*1.25) and self.velocityY > 0):
            self.velocityY=0
        #check on the side
        if((self.is_collision(Map,self.x-self.height*1.25,self.y) and self.velocityX < 0)or (self.is_collision(Map,self.x+self.height*1.25,self.y) and self.velocityX > 0)):
            self.velocityX = 0
        
    def is_collision(self,Map,x,y):
        '''Return True if a plateform is a the coordinate x , y '''
        GroundLayer = Map.Data.get_layer_by_name("Ground")
        # Get coordinate of the tile
        Tile_x = x // Map.tmx_data.tilewidth
        Tile_y = y // Map.tmx_data.tileheight
        for Itile_x, Itile_y, gid in GroundLayer.iter_data():
            if Itile_x == Tile_x and Itile_y == Tile_y:
                #if the tile is not empty 
                return gid != 0
    def check_collision(self, boss):
        '''check collision between boss and apple'''
        player_rect = pygame.Rect(self.x - self.height // 2, self.y - self.height // 2, self.height, self.height)
        boss_rect = pygame.Rect(boss.x, boss.y, boss.width, boss.height)
        #   Boss Collision
        if boss_rect.colliderect(player_rect):
            if self.is_colliding == False :
                self.take_damage(1)
                self.is_colliding = True
        else :
            self.is_colliding = False
        #   Apple Collision
        for apple in boss.Apple:
            apple_rect = pygame.Rect(apple.x,apple.y, apple.height,apple.height)
            if apple_rect.colliderect(player_rect) and apple.damaged == False:
                self.take_damage(1)
                apple.damaged = True

    def take_damage(self, amount):
        self.life -= amount
        if self.life < 0:
            self.life = 0

    def Display(self,screen):
        '''Display player'''
        pygame.draw.circle(screen, "blue", (self.x,self.y), self.height)

