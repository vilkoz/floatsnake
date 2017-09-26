import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class NeuralNet:

    def __init__(self, coefs=0):
        self.sizes ={'X': 48, 'l1': 16, 'l2': 16, 'Y' : 2}
        self.coefs = [None] * 4
        if isinstance(coefs, (np.ndarray, np.generic)):
            self.unroll(coefs)
            print('rolled coefs')
        else:
            self.random_init()

    def random_init(self):
        self.coefs[0] = np.random.random_sample((self.sizes['X'], 1)) - 0.5
        self.coefs[1] = np.random.random_sample((self.sizes['X'], self.sizes['l1'])) - 0.5
        self.coefs[2] = np.random.random_sample((self.sizes['l1'], self.sizes['l2'])) - 0.5
        self.coefs[3] = np.random.random_sample((self.sizes['l2'], self.sizes['Y'])) - 0.5

    def get_output(self, X):
        prev_res = X
        prev_res = prev_res * self.coefs[0].transpose()
        prev_res = sigmoid(prev_res)
        prev_res = prev_res.dot(self.coefs[1])
        prev_res = sigmoid(prev_res)
        prev_res = prev_res.dot(self.coefs[2])
        prev_res = sigmoid(prev_res)
        prev_res = prev_res.dot(self.coefs[3])
        prev_res = sigmoid(prev_res)
        return prev_res[0]

    def roll(self):
        res = []
        for matrix in self.coefs:
            for row in matrix:
                for elem in row:
                    res.append(elem)
        return res

    def unroll(self, array):
        idx = 0
        self.random_init()
        for i in range(self.sizes['X']):
            print('size', self.coefs[0].shape)
            self.coefs[0][i][0] = array[idx]
            idx += 1
        for i in range(self.sizes['X']):
            for j in range(self.sizes['l1']):
                self.coefs[1][i][j] = array[idx]
                idx += 1
        for i in range(self.sizes['l1']):
            for j in range(self.sizes['l2']):
                self.coefs[2][i][j] = array[idx]
                idx += 1
        for i in range(self.sizes['l2']):
            for j in range(self.sizes['Y']):
                self.coefs[3][i][j] = array[idx]
                idx += 1

def test_roll_unroll():
    X0 = np.array([1] * 48 + [2] * 16 * 48 + [3] * 16 * 16 + [4] * 2 * 16)
    X = np.array([1] * 24 + [0] * 24)
    net = NeuralNet(X0)
    a = net.roll()
    print (a)
    print (a.count(1))
    print (a.count(2))
    print (a.count(3))
    print (a.count(4))
    print (net.get_output(X))

if __name__ == "__main__":
    #test_roll_unroll()
    X = np.array([1] * 24 + [-1] * 24)
    X = [0.5] * 32 + [-0.49170078, -0.49170078, -0.49170078, -0.49170078, -0.49170078, -0.49170078, -0.49170078, -0.49170078,
                      -0.49170078, -0.49170078, -0.49170078, -0.49170078, -0.49170078, -0.49170078, -0.49170078, -0.49170078]
    for i in range(100):
        net = NeuralNet()
        print(net.get_output(X))
