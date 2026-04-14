import sympy as sp

x = sp.symbols('x')
expr = x**2+1
print(expr)
f = sp.lambdify(x, expr)
print(f(3))

x, y = sp.symbols('x y')
exp = x+y**2
print(exp)
f1 = sp.lambdify((x, y), exp)
print(f1(2, 3))

"""
#grafica funciones
import numpy as np
import sympy as sp
import matplotlit.pyplot as plt
x = sp.symbols('x')
expr = sp.sin(x)
f = sp.lambdify(x, expr, 'numpy')
xs = np.linspace(0, 10, 100)
ys = f(xs)

plt.plot(xs, ys)
plt.grid()
plt.show()
"""
#Expresar polinomios en pantalla
#import sympy as sp
a = sp.symbols('x')
ex = sp.sin(x+1)
resultado = sp.expand(ex, trig=True)
print(resultado)