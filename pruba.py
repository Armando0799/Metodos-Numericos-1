"""import numpy as np
import matplotlib.pyplot as plt

# Función
def f(x):
    return np.abs(x) + 0.2 * np.sin(10*x)

# Diferencias divididas
def diferencias_divididas(x, y):
    n = len(x)
    coef = np.copy(y)
    
    for j in range(1, n):
        for i in range(n-1, j-1, -1):
            coef[i] = (coef[i] - coef[i-1]) / (x[i] - x[i-j])
    
    return coef

# Evaluación del polinomio de Newton
def newton_eval(x_eval, x, coef):
    n = len(coef)
    p = coef[-1]
    
    for k in range(n-2, -1, -1):
        p = p * (x_eval - x[k]) + coef[k]
    
    return p

# 🔹 Número de puntos
for n in [15, 20]:
    
    # Puntos equiespaciados
    x = np.linspace(-1, 1, n)
    y = f(x)
    
    coef = diferencias_divididas(x, y)
    
    # Para graficar
    x_plot = np.linspace(-1, 1, 400)
    y_real = f(x_plot)
    y_poly = np.array([newton_eval(xi, x, coef) for xi in x_plot])
    
    plt.figure()
    plt.plot(x_plot, y_real, label="f(x)")
    plt.plot(x_plot, y_poly, label="Polinomio Newton")
    plt.scatter(x, y, label="Puntos")
    plt.title(f"Interpolación Newton con {n} puntos (uniformes)")
    plt.legend()
    plt.grid()
    plt.show()"""
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return np.abs(x) + 0.2 * np.sin(10*x)

def diferencias_divididas(x, y):
    n = len(x)
    coef = np.copy(y)
    
    for j in range(1, n):
        for i in range(n-1, j-1, -1):
            coef[i] = (coef[i] - coef[i-1]) / (x[i] - x[i-j])
    
    return coef

def newton_eval(x_eval, x, coef):
    n = len(coef)
    p = coef[-1]
    
    for k in range(n-2, -1, -1):
        p = p * (x_eval - x[k]) + coef[k]
    
    return p

# 🔹 Puntos de Chebyshev
def chebyshev(n):
    k = np.arange(n)
    return np.cos((2*k + 1) * np.pi / (2*n))

# 🔹 Número de puntos
for n in [15, 20]:
    
    x = chebyshev(n)   # ← aquí cambia todo
    y = f(x)
    
    coef = diferencias_divididas(x, y)
    
    x_plot = np.linspace(-1, 1, 400)
    y_real = f(x_plot)
    y_poly = np.array([newton_eval(xi, x, coef) for xi in x_plot])
    
    plt.figure()
    plt.plot(x_plot, y_real, label="f(x)")
    plt.plot(x_plot, y_poly, label="Polinomio Newton")
    plt.scatter(x, y, label="Puntos Chebyshev")
    plt.title(f"Interpolación con {n} puntos (no uniformes)")
    plt.legend()
    plt.grid()
    plt.show()