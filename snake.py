#!./snake/bin/python
import sys
import pygame
import numpy as np
import struct
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
                self.snakes[i] = self.new_best_snake()

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
            if snake != best_snake and snake.points > max_points:
                max_points = snake.points
                second_best_snake = snake
        return (best_snake, second_best_snake)

    def mutate(self, snake):
        genes = snake.nn.roll()
        mutation_possibility = 2 / snake.points
        for gene_i, gene in enumerate(genes):
            byte_string = struct.pack('f', gene)
            byte_list = list(byte_string)
            for i, byte in enumerate(byte_list):
                for j in range(8):
                    if randrange(0, 100000) / 100000 < mutation_possibility:                       byte &= (1 << j)
                byte_list[i] = byte
            genes[gene_i] = struct.unpack('f', bytes(byte_list))
        return genes

    def merge_gens(self, snake1, snake2):
        c1 = self.mutate(snake1)
        c2 = self.mutate(snake2)
        parents = (c1, c2) 
        random_places = [randrange(0, len(c1)) for i in range(12)]
        last_i = 0
        res = []
        cur_parent = 0
        for j in range(len(random_places)):
            for i in range(last_i, random_places[j]):
                res.append(parents[cur_parent][i])
                last_i = i
            cur_parent ^= 1
        for i in range(len(c1)):
            res.append(parents[cur_parent][i])
        return res

    def new_best_snake(self):
        parents = self.get_two_best_snakes()
        print(parents[0].points, parents[1].points)
        new_gene = self.merge_gens(parents[0], parents[1])
        return Snake(randrange(320 - 200, 320 + 200), randrange(240 - 100, 240 + 100), (0, 0, 255), self.screen, new_gene)

    def move_snakes(self):
        for snake in self.snakes:
            X = np.array(snake.gen_inputs(self.food_list))
            X = X / 10000 - 0.5
            # if snake == self.snakes[0]:
            #     print('food', X[:16])
            #     print('gopa', X[16:32])
            #     print('walls', X[32:])
            Y = snake.nn.get_output(X)
            Y = [x / max(Y) for x in Y]
            snake.rotate("left" if Y[0] > Y[1] else "right")
            snake.move()

    def game_loop(self):
        while 1:
            self.screen.fill((0,0,0))
            self.move_snakes()
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
