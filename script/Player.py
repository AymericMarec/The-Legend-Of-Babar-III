import pygame
import time

class Player:
    def __init__(self):
        self.x = 300        
        self.y = 200          
        self.gravity = 30      
        self.speed = 300       
        self.velocityX = 0  
        self.velocityY = 0
        self.MaxJump = 2            
        self.jump = self.MaxJump    
        self.jumpForce = 15         
        self.isfacing = "RIGHT"     
        self.dashspeed = 3          
        self.dashing = False
        self.dashingtime = 10
        self.dashcooldown = 0
        self.height = 20
        self.max_fall_speed = 300

    def Move(self,keys,dt):  
        '''Gestion of the player Movement'''
        if self.dashing :
            self.Dash(dt)
            self.dashingtime -= 1
            if self.dashingtime <= 0 :
                self.dashing = False
                self.dashingtime = 10
        elif self.dashcooldown != 0 : 
            self.dashcooldown -= 1

        if keys[pygame.K_q]:
            # Moving Left
            self.isfacing = "LEFT"
            self.velocityX = -self.speed * dt
        elif keys[pygame.K_d]:
            # Moving Right
            self.isfacing = "RIGHT"
            self.velocityX = self.speed * dt
        elif keys[pygame.K_m]:
            # dashing 
            if not self.dashing and self.dashcooldown == 0:
                self.dashing = True
                self.dashcooldown = 15
        else:
            # if the player don't press any key 
            # stop to movement 
            self.velocityX = 0

        if keys[pygame.K_SPACE] and self.jump >= 1 and not self.velocityY > 0:
            if(self.jump == self.MaxJump):
                self.velocityY = self.jumpForce
            else:
                #double / triple jump less efficient
                self.velocityY = self.jumpForce/1.5
            #remove 1 player jump
            self.jump-=1
        


    def update(self,keys,dt,screen,Map):
        '''Function called every frame in the game'''
        self.Fall(dt,Map)
        self.Move(keys,dt)
        self.Collision_Detection(Map)
        
        self.x += self.velocityX
        self.y -= self.velocityY
        self.Display(screen)

    def Dash(self, dt):
        if self.isfacing == "LEFT" :
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


    def Display(self,screen):
        '''Display player'''
        pygame.draw.circle(screen, "blue", (self.x,self.y), self.height)

