import pygame

class Player:
    def __init__(self):
        self.x = 300
        self.y = 200
        self.velocity = 300
        self.velocityX = 0
        self.velocityY = 0
        self.gravity = 450
        self.height = 20

    def Move(self,keys,dt):
        if keys[pygame.K_a]:
            self.velocityX -= 300 * dt
        if keys[pygame.K_d]:
            self.velocityX += 300 * dt

    def update(self,keys,dt,screen,Map):
        self.velocityX = 0
        self.velocityY = 0
        self.Move(keys,dt)
        self.Fall(dt,Map)
        self.x += self.velocityX
        self.y += self.velocityY
        self.Display(screen)

    def Fall(self,dt,Map):
        if not self.is_Ground(Map) :
            self.velocityY += self.gravity *dt
    def is_Ground(self,Map):
        GroundLayer = Map.Data.get_layer_by_name("Ground")
        Tile_x = self.x // Map.tmx_data.tilewidth
        Tile_y = (self.y+self.height*1.15) // Map.tmx_data.tileheight
        for Itile_x, Itile_y, gid in GroundLayer.iter_data():
            if Itile_x == Tile_x and Itile_y == Tile_y:
                return gid != 0
               
    def Display(self,screen):
        pygame.draw.circle(screen, "blue", (self.x,self.y), self.height)

