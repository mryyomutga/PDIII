import numpy as np

def AND(x1, x2):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.7
    tmp = np.sum(w * x) + b
    if tmp <= 0:
        return 0
    else:
        return 1

def NAND(x1, x2):
    x = np.array([x1, x2])
    w = np.array([-0.5, -0.5])
    b = 0.7
    tmp = np.sum(w * x) + b
    if tmp <= 0:
        return 0
    else:
        return 1

def OR(x1, x2):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.2
    tmp = np.sum(w * x) + b
    if tmp <= 0:
        return 0
    else:
        return 1

def XOR(x1, x2):
    s1 = NAND(x1, x2)
    s2 = OR(x1, x2)
    y = AND(s1, s2)
    return y

if __name__ == "__main__":
    print("input:")
    print("(0,0), (0,1)")
    print("(1,0), (1,1)")
    print("AND Gate")
    print(AND(0,0), AND(0,1))
    print(AND(1,0), AND(1,1))
    print("OR Gate")
    print(OR(0,0), OR(0,1))
    print(OR(1,0), OR(1,1))
    print("NAND Gate")
    print(NAND(0,0), NAND(0,1))
    print(NAND(1,0), NAND(1,1))
    print("XOR Gate")
    print(XOR(0,0), XOR(0,1))
    print(XOR(1,0), XOR(1,1))
