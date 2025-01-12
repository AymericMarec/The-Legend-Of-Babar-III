import pygame
from pytmx import load_pygame
from script.TiledMap import TiledMap
from script.Player import Player
from script.Boss import Boss

class MainGame:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1280, 640))
        pygame.display.set_caption("Snake Battle")
        self.Map = TiledMap("./map/Map.tmx")
        self.player = Player()
        self.boss = Boss()
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.dt = 0

    def game_over_screen(self):
        font = pygame.font.Font(None, 74)
        small_font = pygame.font.Font(None, 36)

        # Affichage du texte Game Over
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(640, 200))
        self.screen.blit(text, text_rect)

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
    def StartGame(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if self.player.life <= 0:
                self.game_over_screen()
                self.player = Player()  # Réinitialiser le joueur
                self.boss = Boss()      # Réinitialiser le boss
                self.Map = TiledMap("./map/SnakeBattle.tmx")
                continue  # Reprendre la boucle principale
            
            keys = pygame.key.get_pressed()
            buttons = pygame.mouse.get_pressed()
            self.Map.draw_map(self.screen)
            self.boss.update(self.player, self.screen, self.dt)
            self.player.update(keys, self.dt, self.screen, self.Map, buttons, self.boss)

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()

if __name__ == "__main__":
    game = MainGame()
    game.StartGame()