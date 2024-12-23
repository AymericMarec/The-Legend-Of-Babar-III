import pygame
from pytmx import load_pygame
from script.TiledMap import TiledMap
from script.Player import Player
from script.Boss import Boss
# pygame setup


pygame.init()

screen = pygame.display.set_mode((1280, 640))
Map = TiledMap("./map/SnakeBattle.tmx")
Player = Player()
Boss = Boss()
clock = pygame.time.Clock()
running = True
dt = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    buttons = pygame.mouse.get_pressed()
    Map.draw_map(screen)
    Player.update(keys,dt,screen,Map,buttons,Boss)
    Boss.update(Player, screen)
        
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()