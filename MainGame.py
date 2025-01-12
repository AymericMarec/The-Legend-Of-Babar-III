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
        self.game_over = False
        self.dt = 0
        self.restart = False

    def game_over_screen(self):
        font = pygame.font.Font(None, 74)
        small_font = pygame.font.Font(None, 36)

        # Affichage du texte Game Over
        self.screen.fill((0, 0, 0))
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(640, 200))
        self.screen.blit(text, text_rect)

        # Bouton Rejouer
        button_text = small_font.render("Rejouer", True, (255, 255, 255))
        button_rect = pygame.Rect(540, 300, 200, 50)
        pygame.draw.rect(self.screen, (0, 128, 0), button_rect)
        self.screen.blit(button_text, button_text.get_rect(center=button_rect.center))
        
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        print("j'ai cliqué")  # Vérifie si le clic est dans le bouton
                        return True

    def win_screen(self):
        font = pygame.font.Font(None, 36)

        # Texte du générique
        credits = [
            "Félicitations !",
            "Vous avez vaincu MOLDORM !",
            "",
            "Équipe de Développement :",
            "          Moi",
            "",
            "THE LEGEND OF BABAR III",
            "",
            "(woula y'aura un 4)"
        ]

        y_offset = 640 

        running = True
        while running:
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Affichage du texte défilant
            for i, line in enumerate(credits):
                text = font.render(line, True, (255, 255, 255))
                text_rect = text.get_rect(center=(640, y_offset + i * 40))
                self.screen.blit(text, text_rect)

            # Défilement vers le haut
            y_offset -= 1

            # Si le générique est entièrement passé, terminer l'écran de victoire
            if y_offset + len(credits) * 40 < 0:
                running = False

            pygame.display.flip()
            self.clock.tick(60)


    def show_start_screen(self):
        font = pygame.font.Font(None, 74)

        # Affichage du texte d'introduction
        self.screen.fill((0, 0, 0))
        text = font.render("THE LEGEND OF BABAR III", True, (255, 255, 255))
        sub_text = font.render("THE RETURN OF MOLDORM", True, (255, 255, 255))
        text_rect = text.get_rect(center=(640, 250))
        sub_text_rect = sub_text.get_rect(center=(640, 350))

        self.screen.blit(text, text_rect)
        self.screen.blit(sub_text, sub_text_rect)
        
        pygame.display.flip()

        # Attendre 3 secondes avant de lancer le jeu
        pygame.time.wait(3000)


    def StartGame(self):
        self.show_start_screen()
        while not self.restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            if self.player.life <= 0:
                self.restart = self.game_over_screen()
            if self.boss.life <= 0:
                self.win_screen()
            keys = pygame.key.get_pressed()
            buttons = pygame.mouse.get_pressed()
            self.Map.draw_map(self.screen)
            self.player.update(keys, self.dt, self.screen, self.Map, buttons, self.boss)
            self.boss.update(self.player, self.screen, self.dt)
            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()

if __name__ == "__main__":
    while True :
        game = MainGame()
        game.StartGame()