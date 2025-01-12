import pygame as pg
from game_objects import *
import sys
from MainGame import MainGame
from time import sleep

class Game:
    def __init__(self):
        pg.init()
        self.WINDOW_SIZE = 700
        self.TILE_SIZE = 50
        self.screen = pg.display.set_mode([self.WINDOW_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.new_game()
    
    def new_game(self):
        self.snake = Snake(self)
        self.food = Food(self)

    def update(self):
        self.snake.update()
        pg.display.flip()
        self.clock.tick(60)

    def draw(self):
        self.screen.fill(('light green'))
        self.food.draw()
        self.snake.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                
            self.snake.control(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            if(len(self.snake.segments)> 5):
                pg.quit()
                sleep(2)
                while True :
                    game = MainGame()
                    game.StartGame()
