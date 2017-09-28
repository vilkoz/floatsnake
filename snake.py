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
        self.modes = {"Evolve": 0, "Play": 1}
        self.mode = 0
        self.is_game_over = False
        self.player_snake = None
        self.KEYS = {'left': 0, 'right': 0}
        self.ticks = pygame.time.get_ticks()

    def check_one_snake_collision(self, snake):
        if snake.check_no_health():
            return True
        self.food_list.collide_snake(snake)
        return False

    def check_all_snakes_collisions(self):
        for i, snake in enumerate(self.snakes):
            if self.check_one_snake_collision(snake):
                if self.mode == self.modes["Play"]:
                    self.is_game_over = True
                self.snakes[i] = self.genetics.new_best_snake()

    def draw_snakes(self):
        for snake in self.snakes:
            if snake == self.genetics.cur_best:
                snake.draw((0, 0, 255))
            else:
                snake.draw()

    def move_snakes(self):
        if self.mode == self.modes["Play"]:
            fps = ((pygame.time.get_ticks() - self.ticks))
        for snake in self.snakes:
            if self.mode == self.modes["Evolve"] or snake != self.player_snake:
                X = np.array(snake.gen_inputs(self.food_list))
                # normalization
                X = X / 10000 - 0.5
                Y = snake.nn.get_output(X)
                angle = snake.get_rotation_angle(Y)
                snake.rotate(angle)
            if self.player_snake and snake == self.player_snake:
                snake.rotate(self.get_user_input_angle() * fps)
            if self.mode == self.modes["Play"]:
                snake.speed = fps / 2
            snake.move()

    def display_info(self):
        pygame.draw.line(self.screen, (255,255,255), (640, 0), (640, 480))
        label = self.font.render((" Mutation pos:   %0.6f" % self.genetics.mutation_possibility), 1, (255,255,255))
        self.screen.blit(label, (640, 10))
        if self.genetics.the_best:
            label = self.font.render((" Record points:  %0.0f" % self.genetics.the_best.points), 1, (255,255,255))
            self.screen.blit(label, (640, 30))
        if self.genetics.cur_best:
            label = self.font.render((" Cur max points: %0.0f" % self.genetics.cur_best.points), 1, (255,255,255))
            self.screen.blit(label, (640, 50))
            label = self.font.render((" Cur max health: %0.0f" % self.genetics.cur_best.health), 1, (255,255,255))
            self.screen.blit(label, (640, 70))

    def switch_modes(self):
        if self.mode == self.modes["Evolve"]:
            if self.genetics.the_best == None:
                return ;
            self.snakes = []
            self.snakes.append(Snake(320, 240, (255, 9, 255), self.screen))
            self.snakes.append(Snake(320, 240, (255, 9, 0), self.screen, self.genetics.the_best.nn.roll()))
            self.player_snake = self.snakes[0]
            self.mode = self.modes["Play"]
            self.is_game_over = False
        elif self.mode == self.modes["Play"]:
            self.mode = self.modes["Evolve"]
            self.snakes = []
            for i in range(10):
                self.snakes.append(self.genetics.new_best_snake())
            self.genetics.snakes = self.snakes
            self.player_snake = None
            self.is_game_over = False

    def handle_key_press(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.KEYS['left'] = 1
                if event.key == pygame.K_RIGHT:
                    self.KEYS['right'] = 1
                if event.key == pygame.K_f:
                    self.switch_modes()
                if event.key == pygame.K_l:
                    self.genetics.evole_from_file()
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.KEYS['left'] = 0
                if event.key == pygame.K_RIGHT:
                    self.KEYS['right'] = 0

    def get_user_input_angle(self):
        angle = 0
        if self.KEYS['left']:
            angle -= 1
        if self.KEYS['right']:
            angle += 1
        return angle

    def update_ticks(self):
        self.ticks = pygame.time.get_ticks()

    def game_loop(self):
        while 1:
            self.screen.fill((0,20,0))
            if self.mode == self.modes["Evolve"] or self.is_game_over == False:
                self.move_snakes()
                self.check_all_snakes_collisions()
                self.genetics.update_current_best()
            self.draw_snakes()
            self.food_list.draw()
            self.display_info()
            self.handle_key_press()
            self.update_ticks()
            pygame.display.update()


def main():
    dojo = Dojo()
    dojo1 = Dojo()
    dojo.game_loop()
    dojo1.game_loop()

if __name__ == "__main__":
    main()
