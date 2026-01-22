import math
import numpy as np
import matplotlib.pyplot as plt

def taylor_raiz(x, n):
    term = 0
    result = 0
    for k in range (1, n):
        term = term * (0.5)-(k-1)*x / k
        result += term
    return result

val_real = math.sqrt(2)
x = 0.5
tolerancia = 0.5e-3