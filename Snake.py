import sys
import pygame
import numpy as np
from math import cos, sin, pi, sqrt, atan2
from random import randrange
from NeuralNet import NeuralNet

def normalize(vector):
    size = sqrt(vector[0]**2 + vector[1]**2)
    if size != 0:
        return [x / size for x in vector]
    else:
        return vector

def distance(node1, node2):
    return sqrt(sum([(x1 - x2) ** 2 for x1, x2 in zip(node1, node2)]))

def sign(num):
    return -1 if num < 0 else 1

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

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
        self.values = []
        self.mean = None
        self.amp = None

    def draw(self, color=None, gradient=True):
        tmp_color = color if color else self.color
        for node in self.chains:
            pygame.draw.circle(self.screen, tmp_color, (int(node[1]), int(node[0])), 10, 0)
            if gradient:
                tmp_color = tuple([(x + 10) if x < 245 else x for x in tmp_color])

    def move(self):
        prev = None
        for node in self.chains:
            if prev == None:
                node[0] += self.speed * self.dir[0]
                node[1] += self.speed * self.dir[1]
            else:
                dist = distance(node, prev)
                if dist > 20:
                    node_speed = dist - 20
                    direction = normalize([x1 - x2 for x1, x2 in zip(prev, node)])
                    node[0] += node_speed * direction[0]
                    node[1] += node_speed * direction[1]
            prev = node
        self.health -= self.speed / 5
        self.points += (self.speed / 5) * 0.1

    def grow(self):
        last = self.chains[-1]
        self.chains.append([x1 - x2 for x1,x2 in zip(last, [x * 20 for x in self.dir])])
        self.health = 100 + 10 * (len(self.chains) - 4)
        self.points += 1

    def rotate(self, angle):
        b = ((angle) / 180) * pi
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

    def intersect_line(self, ray_start, ray_dir, p1, p2):
        ray_start = np.array(ray_start, dtype=np.float)
        ray_dir = np.array(ray_dir, dtype=np.float)
        p1 = np.array(p1, dtype=np.float)
        p2 = np.array(p2, dtype=np.float)
        v1 = ray_start - p1
        v2 = p2 - p1
        v3 = np.array([-ray_dir[1], ray_dir[0]])
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
            dist = distance(point, ray_start)
            if dist < min_dist:
                min_dist = dist
        return min_dist

    def calc_angle(self, ray):
        r1 = self.dir
        r2 = normalize(ray)
        dot = r1[1] * r2[1] + r1[0] * r2[0]
        det = r1[1] * r2[0] - r1[0] * r2[1]
        angle = atan2(det, dot)
        return (angle / (2 * pi)) * 360

    def calc_objects_distances(self, array):
        dist_array = [10000] * 16
        FOV = 90
        for circle in array:
            ray = [x1 - x2 for x1, x2 in zip(circle, self.chains[0])]
            angle = self.calc_angle(ray)
            if angle > -FOV and angle < FOV:
                dist = distance(self.chains[0], circle)
                index = int((angle + FOV) / 16)
                if dist < dist_array[index]:
                    dist_array[index] = dist
        return dist_array

    def gen_inputs(self, food_list):
        rays = []
        for angle in range(-120, 120, 15):
            angle = (angle / 180) * pi
            rays.append(self.rotate_ray(self.dir, angle))
        dist_pear = self.calc_objects_distances([x.pos for x in food_list.list])
        dist_gopa = self.calc_objects_distances(self.chains[1:])
        dist_wall = []
        walls = [[[0,0],[480, 0]],
                [[0,0],[0, 640]],
                [[0,640],[480, 640]],
                [[480,0],[480, 640]]]
        for ray in rays:
            dist_wall.append(self.intersect_line_array(walls, self.chains[0], ray))
        return [-x + 10000 for x in dist_pear] + dist_gopa + dist_wall

    def get_rotation_angle(self, Y):
        if len(self.values) < 10:
            self.values.append(Y)
            return (min(Y) * 60) - 30
        elif self.mean == None:
            v = []
            v.append([x[0] for x in self.values])
            v.append([x[1] for x in self.values])
            self.mean = []
            self.mean.append(mean(v[0]))
            self.mean.append(mean(v[1]))
            self.amp = []
            self.amp.append(max(v[0]) - self.mean[0])
            self.amp.append(max(v[1]) - self.mean[1])
        angle = []
        angle.append(((self.mean[0] - Y[0]) / self.amp[0]) * 90)
        angle.append(((self.mean[1] - Y[1]) / self.amp[1]) * 90)
        return ((angle[0] - angle[1]) / 90) * 15

