import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

def f(x):
    return 1 / (1 + 25 * x**2)


def lagrange(x_eval, x, y):
    n = len(x)
    p = 0
    
    for k in range(n):
        Lk = 1
        for j in range(n):
            if j != k:
                Lk *= (x_eval - x[j]) / (x[k] - x[j])
        p += y[k] * Lk
    
    return p

def lagrange_simbolico(x_vals, y_vals):
    x = sp.Symbol('x')
    n = len(x_vals)
    
    p = 0
    
    for k in range(n):
        Lk = 1
        for j in range(n):
            if j != k:
                Lk *= (x - x_vals[j]) / (x_vals[k] - x_vals[j])
        p += y_vals[k] * Lk
    
    return sp.expand(p)

# Número de puntos
n = 10

x = np.linspace(-1, 1, n+1)
y = f(x)
p = lagrange_simbolico(x, y)

print("\nPolinomio de Lagrange:")
print("="*50)
sp.pprint(p)

x_plot = np.linspace(-1, 1, 200)
y_real = f(x_plot)
y_poly = np.array([lagrange(xi, x, y) for xi in x_plot])

plt.figure()
plt.plot(x_plot, y_real, label="f(x)")
plt.plot(x_plot, y_poly, label="Polinomio")
plt.scatter(x, y, label="Puntos")
plt.legend()
plt.grid()
plt.title("Interpolación de Lagrange")
plt.show()