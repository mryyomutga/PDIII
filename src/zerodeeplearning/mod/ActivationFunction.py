import numpy as np

def step_function(x):
    """Step function"""
    return np.array(x > 0, dtype=np.int)

def sigmoid(x):
    """sigmoid function"""
    return 1 / (1 + np.exp(-x))

def relu(x):
    """relu function"""
    return np.maximum(0, x)

def identity_function(x):
    """identity function"""
    return x
