#!./snake/bin/python
import sys
import pygame
from math import cos, sin, pi, sqrt
from random import randrange

KEYS = {'left': 0, 'right': 0}

def normalize(vector):
    size = sqrt(vector[0]**2 + vector[1]**2)
    return [x / size for x in vector]

def distance(node1, node2):
    return sqrt(sum([(x1 - x2) ** 2 for x1, x2 in zip(node1, node2)]))

class Snake():
    def __init__(self, y0, x0, color, screen):
        self.x = x0
        self.y = y0
        self.color = color
        self.screen = screen
        rand_x = randrange(-100, 100) / 100
        rand_y = randrange(-100, 100) / 100
        self.dir = [rand_y, rand_x]
        self.chains = [[y0, x0]]
        for i in range(3):
            self.grow()
        self.speed = 5
        self.health = 100

    def draw(self):
        for node in self.chains:
            pygame.draw.circle(self.screen, self.color, (int(node[1]), int(node[0])), 10, 0)
        pygame.display.update()

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
        self.health -= 0.5
        self.draw()

    def grow(self):
        last = self.chains[-1]
        self.chains.append([x1 - x2 for x1,x2 in zip(last, [x * 20 for x in self.dir])])

    def rotate(self, text):
        if text == "left":
            b = ((5) / 180) * pi
        elif text == "right":
            b = ((-5) / 180) * pi
        x1 = self.dir[1]
        y1 = self.dir[0]
        self.dir[1] = cos(b) * x1 - sin(b) * y1
        self.dir[0] = sin(b) * x1 + cos(b) * y1
        self.dir = normalize(self.dir)

    def check_no_health(self):
        if self.health <= 0:
            return True
        for node in self.chains:
            if node not in self.chains[0:2] and distance(self.chains[0], node) < 20:
                return True
        return False


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

def check_collisions(snake):
    print('is eat:?', snake.check_no_health())

def main():
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    screen.fill((0,0,0))
    snake = Snake(320, 240, (255, 0, 0), screen)
    while 1:
        screen.fill((0,0,0))
        snake.move()
        pygame.display.update()
        handle_key_press(snake)
        check_collisions(snake)

if __name__ == "__main__":
    main()
