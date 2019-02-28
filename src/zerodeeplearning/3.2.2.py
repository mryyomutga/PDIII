import numpy as np
import matplotlib.pylab as plt

def step(x):
    # if x > 0:
    #     return 1
    # else:
    #     return 0
    return np.array(x > 0, dtype=np.int)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def relu(x):
    return np.maximum(0, x)

x = np.arange(-5.0, 5.0, 0.1)
y = step(x)
plt.plot(x, y)
plt.ylim(-0.1, 1.1)

y = sigmoid(x)
plt.plot(x, y)
plt.ylim(-0.1, 1.1)

y = relu(x)
plt.plot(x, y)
plt.ylim(-0.1, 1.1)

plt.show()