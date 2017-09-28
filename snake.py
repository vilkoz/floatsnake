#!./snake/bin/python
import sys
import pygame
import numpy as np
from math import cos, sin, pi, sqrt
from random import randrange
from Snake import Snake
from Food import Food, FoodList
from Genetics import Genetics

class Dojo:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont("monospace", 15)
        self.screen = pygame.display.set_mode((900,480))
        self.screen.fill((0,0,0))
        self.snakes = []
        for i in range(10):
            self.snakes.append(Snake(320, 240, (255, 9, 0), self.screen))
        self.genetics = Genetics(self)
        self.food_list = FoodList(self.screen)
        self.mutation_possibility = 1 / 800

    def check_one_snake_collision(self, snake):
        if snake.check_no_health():
            return True
        self.food_list.collide_snake(snake)
        return False

    def check_all_snakes_collisions(self):
        for i, snake in enumerate(self.snakes):
            if self.check_one_snake_collision(snake):
                self.snakes[i] = self.genetics.new_best_snake()

    def draw_snakes(self):
        for snake in self.snakes:
            if snake == self.genetics.cur_best:
                snake.draw((0, 0, 255))
            else:
                snake.draw()

    def move_snakes(self):
        for snake in self.snakes:
            X = np.array(snake.gen_inputs(self.food_list))
            # normalization
            X = X / 10000 - 0.5
            Y = snake.nn.get_output(X)
            angle = snake.get_rotation_angle(Y)
            snake.rotate(angle)
            snake.move()

    def display_info(self):
        pygame.draw.line(self.screen, (255,255,255), (640, 0), (640, 480))
        label = self.font.render((" Mutation pos:   %0.6f" % self.mutation_possibility), 1, (255,255,255))
        self.screen.blit(label, (640, 10))
        if self.genetics.the_best:
            label = self.font.render((" Record points:  %0.0f" % self.genetics.the_best.points), 1, (255,255,255))
            self.screen.blit(label, (640, 30))
        if self.genetics.cur_best:
            label = self.font.render((" Cur max points: %0.0f" % self.genetics.cur_best.points), 1, (255,255,255))
            self.screen.blit(label, (640, 50))
            label = self.font.render((" Cur max health: %0.0f" % self.genetics.cur_best.health), 1, (255,255,255))
            self.screen.blit(label, (640, 70))

    def game_loop(self):
        while 1:
            self.screen.fill((0,20,0))
            self.move_snakes()
            self.check_all_snakes_collisions()
            self.genetics.update_current_best()
            self.draw_snakes()
            self.food_list.draw()
            self.display_info()
            pygame.display.update()

KEYS = {'left': 0, 'right': 0}

def handle_key_press(snake):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                KEYS['left'] = 1
            if event.key == pygame.K_RIGHT:
                KEYS['right'] = 1
            if event.key == pygame.K_ESCAPE:
                sys.exit(0)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                KEYS['left'] = 0
            if event.key == pygame.K_RIGHT:
                KEYS['right'] = 0
    if KEYS['left']:
        snake.rotate('left')
    if KEYS['right']:
        snake.rotate('right')

def main():
    dojo = Dojo()
    dojo1 = Dojo()
    dojo.game_loop()
    dojo1.game_loop()

if __name__ == "__main__":
    main()
