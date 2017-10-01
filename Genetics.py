#!./snake/bin/python
import struct
from os import path
from random import randrange
from math import isnan
from Snake import Snake

class Genetics:

    def __init__(self, dojo):
        self.snakes = dojo.snakes
        self.screen = dojo.screen
        self.the_best = None
        self.absolute_best_score = None
        self.absolute_best_coefs = None
        self.load_best_coefs()
        self.second_best = None
        self.cur_best = None
        self.mutation_possibility = 2 / 800

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
        return (self.the_best, self.second_best)

    def random_pick_by_points(self):
        points = [x.points for x in self.snakes]
        s = sum(points)
        points = [x / s for x in points]
        selection = randrange(1000) / 1000
        p_sum = 0
        for i, p in enumerate(points):
            p_sum += p
            if p_sum >= selection:
                return self.snakes[i]

    def random_pick_best_snakes(self):
        return self.random_pick_by_points(), self.random_pick_by_points()

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
        parents = [snake1.nn.roll(), snake2.nn.roll()]
        coefs_len = len(parents[0])
        random_places = [randrange(0, coefs_len) for i in range(12)]
        res = []
        last_i = -1
        cur_parent = 0
        for j in range(len(random_places)):
            for i in range(last_i + 1, random_places[j]):
                byte = self.mutate_byte(parents[cur_parent][i])
                byte = byte[0]
                byte = byte if not isnan(byte) else 0.5
                res.append(byte)
                last_i = i
            cur_parent ^= 1
        for i in range(last_i + 1, coefs_len):
            res.append(parents[cur_parent][i])
        return res

    def new_best_snake(self):
        # parents = self.get_two_best_snakes()
        parents = self.random_pick_best_snakes()
        the_best = self.get_two_best_snakes()[0]
        if the_best.points > self.absolute_best_score:
            self.save_best_coefs(parents[0])
        new_gene = self.merge_gens(parents[0], parents[1])
        return Snake(
            randrange(320 - 200, 320 + 200),
            randrange(240 - 100, 240 + 100),
            (255, 0, 0),
            self.screen,
            net_coefs=new_gene
        )

    def update_current_best(self):
        self.cur_best = [x for x in self.snakes if x.points == max([x.points for x in self.snakes])]
        self.cur_best = self.cur_best[0]

    def load_best_coefs(self):
        if path.isfile('scores.txt'):
            with open('scores.txt') as f:
                m = 0
                m_coefs = []
                for line in f:
                    d = eval(line)
                    if d['points'] > m:
                        m = d['points']
                        m_coefs = d['coefs']
            self.absolute_best_score = m
            self.absolute_best_coefs = m_coefs

    def evole_from_file(self):
        self.load_best_coefs()
        if self.absolute_best_coefs:
            self.the_best = Snake(320, 240, (255, 0, 0), self.screen, self.absolute_best_coefs)

    def save_best_coefs(self, snake):
        with open('scores.txt', 'w') as f:
            f.write(str({'points': snake.points, 'coefs': snake.nn.roll()}) + '\n')

