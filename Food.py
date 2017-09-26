import pygame
from random import randrange
from Snake import distance

class Food():
    def __init__(self, color, screen):
        self.color = color
        self.screen = screen
        self.pos = [randrange(20, 460), randrange(20, 620)]

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.pos[1]), int(self.pos[0])), 5, 0)

class FoodList():

    def __init__(self, screen):
        self.screen = screen
        self.list = []
        for i in range(100):
            self.add_pear()

    def draw(self):
        for pear in self.list:
            pear.draw()

    def add_pear(self):
        self.list.append(Food((255, 255, 0), self.screen))

    def collide_snake(self, snake):
        for pear in self.list:
            for node in snake.chains:
                if distance(node, pear.pos) < 10:
                    if pear in self.list:
                        self.list.remove(pear)
                        self.add_pear()
                        snake.grow()
