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
        self.font = pygame.font.SysFont("monospace", 15)
        self.screen = pygame.display.set_mode((900,480))
        self.screen.fill((0,0,0))
        self.snakes = []
        for i in range(10):
            self.snakes.append(Snake(320, 240, (255, 9, 0), self.screen))
        self.food_list = FoodList(self.screen)
        self.mutation_possibility = 1 / 800
        self.the_best = None
        self.second_best = None
        self.cur_best = None

    def check_one_snake_collision(self, snake):
        if snake.check_no_health():
            return True
        self.food_list.collide_snake(snake)
        return False

    def check_all_snakes_collisions(self):
        for i, snake in enumerate(self.snakes):
            if self.check_one_snake_collision(snake):
                self.snakes[i] = self.new_best_snake()
        self.cur_best = [x for x in self.snakes if x.points == max([x.points for x in self.snakes])]
        self.cur_best = self.cur_best[0]

    def draw_snakes(self):
        for snake in self.snakes:
            if snake == self.cur_best:
                snake.draw((0, 0, 255))
            else:
                snake.draw()

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
        self.mutation_possibility = 1 / (best_snake.points)
        if self.the_best == None or self.the_best.points < best_snake.points:
            self.the_best = best_snake
        else:
            second_best_snake = best_snake
        if self.second_best == None or self.second_best.points < self.second_best.points:
            if second_best_snake != self.the_best:
                self.second_best = second_best_snake
        #return (self.the_best, second_best_snake)
        return (self.the_best, self.second_best)

    def mutate_byte(self, byte):
        byte_list = list(struct.pack('f', byte))
        ret_list = byte_list.copy()
        j = 0
        for b in byte_list:
            for i in range(8):
                if randrange(0, 131072) / 131072 < self.mutation_possibility:
                    ret_list[j] ^= (1 << i)
            j += 1
        return struct.unpack('f', bytes(ret_list))

    def merge_gens(self, snake1, snake2):
        c1 = snake1.nn.roll()
        c2 = snake2.nn.roll()
        parents = (c1, c2) 
        random_places = [randrange(0, len(c1)) for i in range(12)]
        last_i = 0
        res = []
        cur_parent = 0
        for j in range(len(random_places)):
            for i in range(last_i, random_places[j]):
                byte = self.mutate_byte(parents[cur_parent][i])
                res.append(byte)
                last_i = i
            cur_parent ^= 1
        for i in range(len(c1)):
            res.append(parents[cur_parent][i])
        return res

    def new_best_snake(self):
        parents = self.get_two_best_snakes()
        #print(parents[0].points, parents[1].points)
        new_gene = self.merge_gens(parents[0], parents[1])
        return Snake(randrange(320 - 200, 320 + 200), randrange(240 - 100, 240 + 100), (255, 0, 0), self.screen, new_gene)

    def move_snakes(self):
        for snake in self.snakes:
            X = np.array(snake.gen_inputs(self.food_list))
            X = X / 10000 - 0.5
            #if snake == self.snakes[0]:
                #print('inputs', X)
                #print('food', X[:16])
                #print('gopa', X[16:32])
                #print('walls', X[32:])
            Y = snake.nn.get_output(X)
            #Y = [x / max(Y) for x in Y]
            #if snake == self.snakes[0]:
                #print(Y)
            # angle = (Y[0] - Y[1]) * 45
            angle = snake.get_rotation_angle(Y)
            snake.rotate(angle)
            snake.move()

    def display_info(self):
        pygame.draw.line(self.screen, (255,255,255), (640, 0), (640, 480))
        label = self.font.render((" Mutation pos:   %0.6f" % self.mutation_possibility), 1, (255,255,255))
        self.screen.blit(label, (640, 10))
        if self.the_best:
            label = self.font.render((" Record points:  %0.0f" % self.the_best.points), 1, (255,255,255))
            self.screen.blit(label, (640, 30))
        if self.cur_best:
            label = self.font.render((" Cur max points: %0.0f" % self.cur_best.points), 1, (255,255,255))
            self.screen.blit(label, (640, 50))
            label = self.font.render((" Cur max health: %0.0f" % self.cur_best.health), 1, (255,255,255))
            self.screen.blit(label, (640, 70))

    def game_loop(self):
        while 1:
            self.screen.fill((0,20,0))
            self.move_snakes()
            self.check_all_snakes_collisions()
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
    dojo.game_loop()

if __name__ == "__main__":
    main()
