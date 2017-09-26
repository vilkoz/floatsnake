import sys
import pygame
import numpy as np
from math import cos, sin, pi, sqrt
from random import randrange
from NeuralNet import NeuralNet

def normalize(vector):
    size = sqrt(vector[0]**2 + vector[1]**2)
    return [x / size for x in vector]

def distance(node1, node2):
    return sqrt(sum([(x1 - x2) ** 2 for x1, x2 in zip(node1, node2)]))

def sign(num):
    return -1 if num < 0 else 1

def ray_cmp(v1, v2):
    v1 = normalize(v1)
    v2 = normalize(v2)
    for x1, x2 in zip(v1, v2):
        if abs((x1) - (x2)) >= 0.00001:
            return False
    return True

class Snake():
    def __init__(self, y0, x0, color, screen, net_coefs=None):
        self.color = color
        self.screen = screen
        rand_x = randrange(-100, 100) / 100
        rand_y = randrange(-100, 100) / 100
        self.dir = normalize([rand_y, rand_x])
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
        self.health -= 1
        self.points += 5
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
        self.dir = self.rotate_ray(self.dir, b)
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

    def rotate_ray(self, ray, angle):
        return [sin(angle) * ray[1] + cos(angle) * ray[0], cos(angle) * ray[1] - sin(angle) * ray[0]]

    def intersect_circle(self, ray_start, ray_dir, center, radius):
        ray_end = [x1 + x2 for x1, x2 in zip(ray_start, ray_dir)]
        dx = ray_end[1] - ray_start[1]
        dy = ray_end[0] - ray_start[0]
        dr = sqrt(dx * dx + dy * dy)
        D = ray_start[1] * ray_end[0] - ray_end[1] * ray_start[0]
        delta = (radius ** 2) * (dr ** 2) - (D ** 2)
        if delta < 0:
            return None
        else:
            return [
                    [((-D * dx) + (abs(dx) * sqrt(delta))) / (dr ** 2), 
                    ((D * dy) + (sign(dy) * (dx) * sqrt(delta))) / (dr ** 2)],
                    [((-D * dx) - (abs(dx) * sqrt(delta))) / (dr ** 2), 
                    ((D * dy) - (sign(dy) * (dx) * sqrt(delta))) / (dr ** 2)],
                    ]

    def intersect_line(self, ray_start, ray_dir, p1, p2):
        ray_start = np.array(ray_start, dtype=np.float)
        ray_dir = np.array(ray_dir, dtype=np.float)
        p1 = np.array(p1, dtype=np.float)
        p2 = np.array(p2, dtype=np.float)
        v1 = ray_start - p1
        v2 = p2 - p1
        v3 = np.array([-ray_dir[0], ray_dir[1]])
        t1 = np.cross(v2, v1) / np.dot(v2, v3)
        t2 = np.dot(v1, v3) / np.dot(v2, v3)
        if t1 >= 0.0 and t2 >= 0.0 and t2 <= 1.0:
            res = ray_start + t1 * ray_dir
            return res.tolist()
        return None

    def intersect_line_array(self, array, ray_start, ray_dir):
        min_dist = 1000
        for line in array:
            point = self.intersect_line(ray_start, ray_dir, line[1], line[0])
            if point == None:
                continue
            if distance(point, ray_start) < min_dist:
                min_dist = distance(point, ray_start)
        return min_dist

    def intersect_circle_array(self, array, radius, ray, ray_start):
        min_dist = 10000
        for circle in array:
            points = self.intersect_circle(ray_start, ray, circle, radius)
            if points == None:
                continue
            [p1, p2] = points
            if distance(p1, self.chains[0]) > distance(p2, self.chains[0]):
                p = p2
            else:
                p = p1
            dist = distance(p, self.chains[0])
            # if ray_cmp([x1 - x2 for x1, x2 in zip(p, self.chains[0])], ray) and dist < min_dist:
            if dist < min_dist:
                min_dist = dist
        return min_dist

    def gen_inputs(self, food_list):
        rays = []
        for angle in range(-120, 120, 15):
            angle = (angle / 180) * pi
            rays.append(self.rotate_ray(self.dir, angle))
        dist_pear = []
        dist_gopa = []
        dist_wall = []
        walls = [[[0,0],[480, 0]],
                [[0,0],[0, 640]],
                [[0,640],[480, 640]],
                [[480,0],[480, 640]]]
        for ray in rays:
            dist_pear.append(self.intersect_circle_array(food_list.list, 5, ray, self.chains[0]))
            dist_gopa.append(self.intersect_circle_array(self.chains[1:], 10, ray, self.chains[0]))
            dist_wall.append(self.intersect_line_array(walls, self.chains[0], self.dir))
        return dist_pear + dist_gopa + dist_wall

