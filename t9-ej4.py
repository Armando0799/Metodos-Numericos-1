import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return np.abs(x)+0.2*np.sin(10*x)

def dif_div(x, y):
    n = len(x)
    vector = np.copy(y)
    for j in range(1, n):
        for i in range(n-1, j-1, -1):
            vector[i] = (vector[i]-vector[i-1])/(x[i]-x[i-j])

    return vector

def pol_newton(xv, x, vector):
    n = len(vector)
    p = vector[-1]
    for k in range(n-2, -1, -1):
        p = p * (xv - x[k]) + vector[k]

    return p

def desuniforme(n):
    k = np.arange(n)
    return np.cos((2*k+1) * np.pi / (2*n))

for n in [15, 20]:
    x = desuniforme(n)
    y = f(x)
    coefi = dif_div(x, y)

    xgraf = np.linspace(-1, 1, 400)
    yreal = f(xgraf)
    ygraf = np.array([pol_newton(xi, x, coefi) for xi in xgraf])

    plt.figure()
    plt.plot(xgraf, yreal, label='f(x)')
    plt.plot(xgraf, ygraf, label='Polinomio de newton')
    plt.scatter(x, y, label='Puntos')
    plt.title(f"Interpolacion de newton con {n} puntos no uniformes")
    plt.legend()
    plt.grid()
    plt.show()