import numpy as np

def sigmoid(x, deriv=False):
    if (deriv):
        return x * (1-x)
    return 1 / (1 + np.exp(-x))

class NeuralNet:

    def __init__(self, coefs=0):
        self.sizes ={'X': 48, 'l1': 16, 'l2': 16, 'Y' : 2}
        self.coefs = [None] * 4
        # if isinstance(coefs, (np.ndarray, np.generic)):
        if not isinstance(coefs, int):
            self.random_init()
            self.unroll(coefs)
        else:
            self.random_init()

    def random_init(self):
        self.coefs[0] = np.random.random_sample((self.sizes['X'], 1)) - 0.5
        self.coefs[1] = np.random.random_sample((self.sizes['X'], self.sizes['l1'])) - 0.5
        self.coefs[2] = np.random.random_sample((self.sizes['l1'], self.sizes['l2'])) - 0.5
        self.coefs[3] = np.random.random_sample((self.sizes['l2'], self.sizes['Y'])) - 0.5

    def get_output(self, X):
        prev_res = X
        # prev_res = prev_res * self.coefs[0].transpose()
        # prev_res = sigmoid(prev_res)
        prev_res = prev_res.dot(self.coefs[1])
        prev_res = sigmoid(prev_res)
        prev_res = prev_res.dot(self.coefs[2])
        prev_res = sigmoid(prev_res)
        prev_res = prev_res.dot(self.coefs[3])
        prev_res = sigmoid(prev_res)
        # return prev_res[0]
        return prev_res

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
        if len(array) != (48 + 48 * 16 + 16 * 16 + 16 * 2):
            print('unroll array size:', len(array), 'expected:', 48 + 48 * 16 + 16 * 16 + 16 * 2 )
        for i in range(self.sizes['X']):
            self.coefs[0][i] = array[idx]
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

    def train(self, X, Y, epochs=6000, lr=0.01):
        layers = [None] * 5
        errors = [None] * 5
        deltas = [None] * 4
        for _ in range(epochs):
            layers[0] = X # 48 x 1000
            layers[1] = sigmoid(layers[0].dot(self.coefs[1])) # 16 x 1000
            layers[2] = sigmoid(layers[1].dot(self.coefs[2])) # 16 x 1000
            layers[3] = sigmoid(layers[2].dot(self.coefs[3])) # 2 x 1000

            errors[3] = Y - layers[3] # 2 x 1082
            print("\rError: ", np.mean(np.abs(errors[3])), end='')
            deltas[3] = errors[3] * sigmoid(layers[3], deriv=True)
            errors[2] = deltas[3].dot(self.coefs[3].T)
            deltas[2] = errors[2] * sigmoid(layers[2], deriv=True)
            errors[1] = deltas[2].dot(self.coefs[2].T)
            deltas[1] = errors[1] * sigmoid(layers[1], deriv=True)
            errors[0] = deltas[1].dot(self.coefs[1].T)
            deltas[0] = errors[0] * sigmoid(layers[0], deriv=True)

            self.coefs[3] += layers[2].T.dot(deltas[3]) * lr
            self.coefs[2] += layers[1].T.dot(deltas[2]) * lr
            # print(self.coefs[1].shape, layers[0].shape, deltas[1].shape)
            self.coefs[1] += layers[0].T.dot(deltas[1]) * lr
            # self.coefs[0] += X.T * deltas[0].T


def test_roll_unroll():
    X0 = np.array([1] * 48 + [2] * 16 * 48 + [3] * 16 * 16 + [4] * 2 * 16)
    X = np.array([1] * 24 + [0] * 24)
    net = NeuralNet(X0)
    a = net.roll()
    print (a)
    # print ('48:',a.count(1))
    # print ('16:',a.count(2))
    # print ('16:',a.count(3))
    # print ('2:',a.count(4))
    print (net.unroll(a))
    print (net.coefs)
    # print (net.get_output(X))

if __name__ == "__main__":
    test_roll_unroll()
    # X = np.array([1] * 24 + [-1] * 24)
    # X = [0.5] * 32 + [-0.49170078, -0.49170078, -0.49170078, -0.49170078, -0.49170078, -0.49170078, -0.49170078, -0.49170078,
    #                   -0.49170078, -0.49170078, -0.49170078, -0.49170078, -0.49170078, -0.49170078, -0.49170078, -0.49170078]
    # for i in range(100):
    #     net = NeuralNet()
    #     print(net.get_output(X))
