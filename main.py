import pygame
from pytmx import load_pygame
from script.TiledMap import TiledMap
from script.Player import Player
# pygame setup


pygame.init()

screen = pygame.display.set_mode((1280, 640))
Map = TiledMap("./map/SnakeBattle.tmx")
Player = Player()
clock = pygame.time.Clock()
running = True
dt = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    
    Map.draw_map(screen)
    Player.update(keys,dt,screen,Map)
    # print(Map.tmx_data.get_tile_properties(Player.x/128,Player.y/128,1))
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()