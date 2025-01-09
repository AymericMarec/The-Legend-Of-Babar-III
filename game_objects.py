import pygame as pg
from random import randrange

vec2 = pg.math.Vector2

class Snake :
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        self.rect.center = self.get_random_position()
        self.direction = vec2(0, 0)
        self.step_delay = 100
        self.time = 0
        self.lenght = 1
        self.segments = []
        self.directions = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
        
    def control(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_z and self.directions[pg.K_w]:
                self.direction = vec2(0, -self.size)
                self.directions = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
                
            if event.key == pg.K_s:
                self.direction = vec2(0, self.size)
                self.directions = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
                
            if event.key == pg.K_q:
                self.direction = vec2(-self.size, 0)
                self.directions = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
                
            if event.key == pg.K_d:
                self.direction = vec2(self.size, 0)
                self.directions = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}
    
    def delta_time(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time >= self.step_delay:
            self.time = time_now
            return True
        return False
        
    def get_random_position(self):
        return [randrange(self.size // 2, self.game.WINDOW_SIZE - self.size // 2, self.size)] * 2
    
    def check_borders(self):
        if self.rect.left < 0 or self.rect.right > self.game.WINDOW_SIZE:
            self.game.new_game()
        if self.rect.top < 0 or self.rect.bottom > self.game.WINDOW_SIZE:
            self.game.new_game()
    
    def check_food(self):
        if self.rect.center == self.game.food.rect.center :
            self.game.food.rect.center = self.get_random_position()
            self.lenght += 1
            
    def check_selfeating(self):
        if len(self.segments) != len(set(segment.center for segment in self.segments)):
                self.game.new_game()
    
    def move(self):
        if self.delta_time():
            self.rect.move_ip(self.direction)
            self.segments.insert(0, self.rect.copy())
            self.segments = self.segments[:self.lenght]
    
    def update(self):
        self.check_selfeating()
        self.check_borders()
        self.check_food()
        self.move()

    def draw(self):
        time = pg.time.get_ticks() / 1000
        moldorm_colors = [
            (255, 69, 0),
            (255, 215, 0),
        ]
        
        for i, segment in enumerate(self.segments):
            if i == 0:
                color = moldorm_colors[0]
            else:
                base_color = moldorm_colors[(i % (len(moldorm_colors) - 1)) + 1]
                color = tuple(int(c) for c in base_color)
            
            pg.draw.rect(self.game.screen, color, segment)

class Food:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.image = pg.image.load('assets/apple.png')
        self.image = pg.transform.scale(self.image, (self.size - 2, self.size - 2))
        self.rect = self.image.get_rect()
        self.rect.center = self.game.snake.get_random_position()

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

