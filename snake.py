#!./snake/bin/python
import sys
import pygame
from math import cos, sin, pi, sqrt
from random import randrange
from Snake import Snake
from Food import Food, FoodList

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

def check_collisions(snake, food_list):
    if snake.check_no_health():
        return True
    food_list.collide_snake(snake)
    return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    screen.fill((0,0,0))
    snake = Snake(320, 240, (255, 0, 0), screen)
    food_list = FoodList(screen)
    while 1:
        screen.fill((0,0,0))
        snake.move()
        handle_key_press(snake)
        if check_collisions(snake, food_list):
            snake = Snake(320, 240, (255, 0, 0), screen)
        food_list.draw()
        pygame.display.update()

if __name__ == "__main__":
    main()
