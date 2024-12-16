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


tmxdata = load_pygame("./map/SnakeBattle.tmx")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()
    
    Map.draw_map(screen)
    Player.Move(keys,dt)
    pygame.draw.circle(screen, "red", (Player.x,Player.y), 40)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()