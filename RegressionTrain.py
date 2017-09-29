import numpy
import pygame
from Snake import Snake
from snake import Dojo
from SupervisedDojo import SupervisedDojo

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

class TrainedNN:

    def __init__(self, model):
        self.model = model

    def get_output(self, X):
        array = numpy.array(X)
        a = self.model.predict(numpy.expand_dims(array, axis=0))
        a = a.tolist()
        return a[0]

class TrainedSnake(Snake):
    def __init__(self, y0, x0, color, screen, model):
        super().__init__(y0, x0, color, screen)
        self.nn = TrainedNN(model)
        tryes = [None] * 100
        # for i in range(100):
        #     y = model.predict(numpy.expand_dims(numpy.random.random_sample((48)), axis=0))
        #     tryes[i] = y[0][0]
        # self.mean = mean(tryes)
        # self.max = max(tryes)

    # def get_rotation_angle(self, Y):
    #     angle = (Y[0] - self.mean) / (self.max - self.mean)
    #     return angle * 15

class TestDojo(Dojo):

    def __init__(self, model):
        super().__init__()
        self.snakes = []
        self.model = model
        for i in range(2):
            self.snakes.append(TrainedSnake(320, 240, (255, 9, 255), self.screen, model))

    def display_info(self):
        pygame.draw.line(self.screen, (255,255,255), (640, 0), (640, 480))
        label = self.font.render((" Snake1 points:  %0.0f" % self.snakes[0].points), 1, (255,255,255))
        self.screen.blit(label, (640, 10))
        label = self.font.render((" Snake1 health:  %0.0f" % self.snakes[0].health), 1, (255,255,255))
        self.screen.blit(label, (640, 30))
        label = self.font.render((" Snake2 points:  %0.0f" % self.snakes[1].points), 1, (255,255,255))
        self.screen.blit(label, (640, 50))
        label = self.font.render((" Snake2 health:  %0.0f" % self.snakes[1].health), 1, (255,255,255))
        self.screen.blit(label, (640, 30))

    def check_all_snakes_collisions(self):
        for i, snake in enumerate(self.snakes):
            if self.check_one_snake_collision(snake):
                if self.mode == self.modes["Play"]:
                    self.is_game_over = True
                self.snakes[i] = TrainedSnake(320, 240, (255, 9, 255), self.screen, self.model)

def baseline_model():
    from keras.models import Sequential
    from keras.layers import Dense, Activation
    model = Sequential()
    model.add(Dense(16, input_dim=48, kernel_initializer='normal', activation='relu'))
    model.add(Activation('sigmoid'))
    model.add(Dense(16, kernel_initializer='normal'))
    model.add(Activation('sigmoid'))
    model.add(Dense(2, kernel_initializer='normal'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

def train_model(data):
    print("[.] Starting loading data")
    a = data
    if len(a[0]) < 1000:
        print("[!] Not enough data for train, loading from data.txt")
        with open('data.txt') as f:
            a = []
            for line in f:
                a.append(eval(line))

    X = [x[0] for x in a[0]]
    Y = [x[1] for x in a[0]]
    X = numpy.array(X)
    Y = numpy.array(Y)
    print("[+] Loaded data")
    print("[.] Running training")
    model = baseline_model()
    model.fit(X, Y, epochs=10, batch_size=32)
    results = model.evaluate(X, Y, batch_size=128)
    print("\nres: ", results)
    for i, x in enumerate(X):
        print(model.predict(numpy.expand_dims(x, axis=0)), Y[i])
    return model

def main():
    supervised_dojo = SupervisedDojo()
    data = supervised_dojo.game_loop()
    model = train_model(data)
    print(model.summary())
    dojo = TestDojo(model)
    dojo.game_loop()

if __name__ == "__main__":
    main()
