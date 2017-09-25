import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class NeuralNet:

    def __init__(self):
        self.sizes ={'X': 48, 'l1': 16, 'l2': 16, 'Y' : 2}
        self.coefs = [None] * 4
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
        print('nn out', prev_res)
        return prev_res

    def roll(self):
        res = None
        for matrix in self.coefs:
            if not None:
                res = matrix.tolist()
            else:
                res = np.append(res, matrix.tolist())
        return res

    def unroll(self, array):
        idx = 0
        for i in range(self.sizes['X']):
            self.coefs[0][0][i] = array[idx]
            idx += 1
        for i in range(self.sizes['X'], self.sizes['l1']):
            for j in range(self.sizes['l1']):
                self.coefs[1][i][j] = array[idx]
                idx += 1
        for i in range(self.sizes['l1'], self.sizes['l2']):
            for j in range(self.sizes['l2']):
                self.coefs[2][i][j] = array[idx]
                idx += 1
        for i in range(self.sizes['l2'], self.sizes['Y']):
            for j in range(self.sizes['Y']):
                self.coefs[3][i][j] = array[idx]
                idx += 1

if __name__ == "__main__":
    X0 = np.array([1 for x in range(0, 48)], float, ndmin=2)
    net = NeuralNet()
    print(net.get_output(X0))
