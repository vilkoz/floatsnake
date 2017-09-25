import sys
import pygame
from math import cos, sin, pi, sqrt
from random import randrange
from NeuralNet import NeuralNet

def normalize(vector):
    size = sqrt(vector[0]**2 + vector[1]**2)
    return [x / size for x in vector]

def distance(node1, node2):
    return sqrt(sum([(x1 - x2) ** 2 for x1, x2 in zip(node1, node2)]))

class Snake():
    def __init__(self, y0, x0, color, screen, net_coefs=None):
        self.x = x0
        self.y = y0
        self.color = color
        self.screen = screen
        rand_x = randrange(-100, 100) / 100
        rand_y = randrange(-100, 100) / 100
        self.dir = [rand_y, rand_x]
        self.chains = [[y0, x0]]
        self.points = 0
        for i in range(3):
            self.grow()
        self.speed = 5
        self.rot_speed = 5
        self.health = 100
        self.nn = NeuralNet(net_coefs)

    def draw(self):
        for node in self.chains:
            pygame.draw.circle(self.screen, self.color, (int(node[1]), int(node[0])), 10, 0)

    def move(self):
        prev = None
        for node in self.chains:
            if prev == None:
                node[0] += self.speed * self.dir[0]
                node[1] += self.speed * self.dir[1]
            else:
                if distance(prev, node) > 20:
                    direction = normalize([x1 - x2 for x1, x2 in zip(prev, node)])
                    node[0] += self.speed * direction[0]
                    node[1] += self.speed * direction[1]
            prev = node
        self.health -= 0.1
        self.points += 5
        print('snake move')
        self.draw()

    def grow(self):
        last = self.chains[-1]
        self.chains.append([x1 - x2 for x1,x2 in zip(last, [x * 20 for x in self.dir])])
        self.health = 100
        self.points += 100

    def rotate(self, text):
        if text == "left":
            b = ((self.rot_speed) / 180) * pi
        elif text == "right":
            b = ((-self.rot_speed) / 180) * pi
        x1 = self.dir[1]
        y1 = self.dir[0]
        self.dir[1] = cos(b) * x1 - sin(b) * y1
        self.dir[0] = sin(b) * x1 + cos(b) * y1
        self.dir = normalize(self.dir)

    def check_no_health(self):
        pos = self.chains[0]
        if pos[1] < 10 or pos[1] > 630 or pos[0] < 10 or pos[0] > 470:
            return True
        if self.health <= 0:
            return True
        for node in self.chains:
            if node not in self.chains[0:2] and distance(self.chains[0], node) < 20:
                return True
        return False
