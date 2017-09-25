#!./snake/bin/python
import sys
import pygame
from math import cos, sin, pi, sqrt
from random import randrange
from Snake import Snake
from Food import Food, FoodList

class Dojo:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640,480))
        self.screen.fill((0,0,0))
        self.snakes = []
        for i in range(10):
            self.snakes.append(Snake(320, 240, (255, 9, 0), self.screen))
        self.food_list = FoodList(self.screen)

    def check_one_snake_collision(self, snake):
        if snake.check_no_health():
            return True
        self.food_list.collide_snake(snake)
        return False

    def check_all_snakes_collisions(self):
        for i, snake in enumerate(self.snakes):
            if self.check_one_snake_collision(snake):
                self.snakes[i] = Snake(320, 240, (255, 0, 0), self.screen)

    def get_two_best_snakes(self):
        max_points = 0
        best_snake = None
        for snake in self.snakes:
            if snake.points > max_points:
                max_points = snake.points
                best_snake = snake
        max_points = 0
        second_best_snake = None
        for snake in self.snakes:
            if snake.points > max_points:
                max_points = snake.points
                second_best_snake = snake
        return (best_snake, second_best_snake)

    def new_best_snake(self):
        best_snakes = self.get_two_best_snakes()

    def game_loop(self):
        while 1:
            self.screen = pygame.display.set_mode((640,480))
            self.screen.fill((0,0,0))
            for snake in self.snakes:
                snake.move()
            self.check_all_snakes_collisions()
            self.food_list.draw()
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
    dojo.game_loop()

if __name__ == "__main__":
    main()
