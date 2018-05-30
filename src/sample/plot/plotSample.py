import os
import time
from multiprocessing import Process, Pipe

import numpy as np
import matplotlib.pyplot as plt

def func1():
    fig = plt.figure()
    plt.ion()
    x = list()
    y = list()

    parent, child = Pipe()
    cp = Process(target=func2,args=(child,))
    cp.start()
    while True:
        temp = parent.recv()
        x.append(np.cos(temp) * 2)
        y.append(np.sin(temp) * 2)
        plt.scatter(x, y)
        plt.show()
        plt.pause(0.01)
    cp.join()

def func2(pipe):
    while True:
        p = np.random.uniform(-np.pi, np.pi, 1)
        pipe.send(p)
        time.sleep(1)

if __name__ == "__main__":
    p = Process(target=func1)
    p.start()
    p.join()
