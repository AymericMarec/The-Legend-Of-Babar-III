import pygame
from pytmx import load_pygame
from script.TiledMap import TiledMap
from script.Player import Player
from script.Boss import Boss

pygame.init()

screen = pygame.display.set_mode((1280, 640))
pygame.display.set_caption("Snake Battle")
Map = TiledMap("./map/SnakeBattle.tmx")
player = Player()
boss = Boss()
clock = pygame.time.Clock()
running = True
game_over = False
dt = 0

def game_over_screen(screen):
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

    # Affichage du texte Game Over
    text = font.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=(640, 200))
    screen.blit(text, text_rect)

    # # Bouton Rejouer
    # button_text = small_font.render("Rejouer", True, (255, 255, 255))
    # button_rect = pygame.Rect(540, 300, 200, 50)
    # pygame.draw.rect(screen, (0, 128, 0), button_rect)
    # screen.blit(button_text, button_text.get_rect(center=button_rect.center))
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if player.life <= 0:
        game_over_screen(screen)
        player = Player()  # Réinitialiser le joueur
        boss = Boss()      # Réinitialiser le boss
        Map = TiledMap("./map/SnakeBattle.tmx")
        continue  # Reprendre la boucle principale
    
    keys = pygame.key.get_pressed()
    buttons = pygame.mouse.get_pressed()
    Map.draw_map(screen)
    boss.update(player, screen, dt)
    player.update(keys, dt, screen, Map, buttons, boss)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
