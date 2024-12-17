import pygame

class Player:
    def __init__(self):
        self.x = 300
        self.y = 200
        self.gravity = 500
        self.jump_height = 60
        self.speed = 300
        self.velocityX = 0
        self.velocityY = 0
        self.jump = 1 # 2
        self.isjumping = False
        
        self.height = 20
        

    def Move(self,keys,dt):
        
        if self.isjumping :
            # self.y -= self.velocityY
            print(dt)
            self.velocityY -= self.gravity
            if self.velocityY < -self.jump_height:
                self.isjumping = False
                self.velocityY = self.jump_height
        if keys[pygame.K_a]:
            self.velocityX -= self.speed * dt
        if keys[pygame.K_d]:
            self.velocityX += self.speed * dt
        if keys[pygame.K_SPACE] and not self.isjumping and self.jump > 0:
            self.jump -= 1
            self.isjumping = True
            # self.jumping_time = 15
    def update(self,keys,dt,screen,Map):
        self.velocityX = 0
        self.velocityY = 0
        self.Move(keys,dt)
        self.Fall(dt,Map)
        # self.Fall(dt,Map)
        self.x += self.velocityX
        self.y -= self.velocityY
        self.Display(screen)

    def Fall(self,dt,Map):
        if not self.is_Ground(Map) :
            self.velocityY -= self.gravity *dt
        else :
            self.jump = 1
    def is_Ground(self,Map):
        GroundLayer = Map.Data.get_layer_by_name("Ground")
        Tile_x = self.x // Map.tmx_data.tilewidth
        Tile_y = (self.y+self.height*1.15) // Map.tmx_data.tileheight
        for Itile_x, Itile_y, gid in GroundLayer.iter_data():
            if Itile_x == Tile_x and Itile_y == Tile_y:
                return gid != 0
               
    def Display(self,screen):
        pygame.draw.circle(screen, "blue", (self.x,self.y), self.height)

