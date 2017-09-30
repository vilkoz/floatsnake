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
        array = numpy.array(X) / 10000
        a = self.model.predict(numpy.expand_dims(array, axis=0))
        a = a.tolist()
        return a[0]

class TrainedSnake(Snake):
    def __init__(self, y0, x0, color, screen, model):
        super().__init__(y0, x0, color, screen)
        # self.nn = TrainedNN(model)
        self.nn = model
        # tryes = [None] * 100
        # for i in range(100):
        #     # y = model.predict(numpy.expand_dims(numpy.random.random_sample((48)), axis=0))
        #     tryes[i] = y[0][0]
        # self.mean = mean(tryes)
        # self.max = max(tryes)

    # def get_rotation_angle(self, Y):
    #     angle = (Y[0] - self.mean) / (self.max - self.mean)
    #     # angle = Y[0]
    #     # i, val = max(enumerate(Y))
    #     # angle = (i*2 - 1) * 5
    #     return angle

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
        self.screen.blit(label, (640, 70))

    def check_all_snakes_collisions(self):
        for i, snake in enumerate(self.snakes):
            if self.check_one_snake_collision(snake):
                if self.mode == self.modes["Play"]:
                    self.is_game_over = True
                self.snakes[i] = TrainedSnake(320, 240, (255, 9, 255), self.screen, self.model)

def loss_func(y_true, y_pred):
    y_true = y_true.eval().tolist()
    y_pred = y_pred.eval().tolist()
    res = []
    for x1, x2 in zip(y_true, y_pred):
        i, val = max(enumerate(x1))
        res.append(x2[i])
    return mean(res)

def baseline_model():
    from keras.models import Sequential
    from keras.layers import Dense, Activation
    from keras import optimizers
    model = Sequential()
    model.add(Dense(64, input_dim=48, activation='relu'))
    # model.add(Dense(16, input_dim=48, kernel_initializer='normal', activation='relu'))
    # model.add(Activation('relu'))
    model.add(Dense(64))
    # model.add(Activation('sigmoid'))
    # model.add(Activation('tanh'))
    # model.add(Dense(2, kernel_initializer='normal'))
    model.add(Dense(2, activation='softmax'))
    # model.compile(loss='binary_crossentropy', optimizer=optimizers.Adam(lr=0.001))
    model.compile(loss='hinge', optimizer=optimizers.Adam(lr=0.001))
    return model

def own_model():
    from NeuralNet import NeuralNet
    net = NeuralNet()
    return net

def train_model(data):
    print("[.] Starting loading data")
    a = data
    if len(a[0]) < 1000:
        print("[!] Not enough data for train, loading from data.txt")
        with open('data.txt') as f:
            a = []
            for line in f:
                a.append(eval(line))

    X = numpy.array([x[0] for x in a[0]])
    Y = numpy.array([x[1] for x in a[0]])
    print("[+] Loaded data")
    print("[.] Running training")
    # model = baseline_model()
    # model.fit(X, Y, epochs=10, batch_size=32, verbose=2)
    # results = model.evaluate(X, Y, batch_size=128)
    model = own_model()
    model.train(X, Y, lr=0.01, epochs=100)
    # print("\nres: ", results)
    for i, x in enumerate(X):
        # print(model.predict(numpy.expand_dims(x, axis=0)), Y[i])
        # print(x)
        print(model.get_output(x), Y[i])
    return model

def main():
    supervised_dojo = SupervisedDojo()
    data = supervised_dojo.game_loop()
    model = train_model(data)
    # print(model.summary())
    dojo = TestDojo(model)
    dojo.game_loop()

if __name__ == "__main__":
    main()
