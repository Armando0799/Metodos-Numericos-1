"""
Utiliza x0=2, x1=2.5 y x2=4 para obtener el segundo polinomio de lagangre para
f(x)=1/x. graficar el polinomio y la funcion 1/x.
"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt


x0, x1, x2, x = sp.symbols('x0 x1 x2 x')
l0 = (((x-x1)/(x0-x1))*((x-x2)/(x0-x2)))*(1/x0)
l1 = (((x-x0)/(x1-x0))*((x-x2)/(x1-x2)))*(1/x1)
l2 = (((x-x0)/(x2-x0))*((x-x1)/(x2-x1)))*(1/x2)

f0 = sp.lambdify((x0, x1, x2), l0)
res_l0 = sp.expand(f0(2, 2.5, 4), trig=True)

f1 = sp.lambdify((x0, x1, x2), l1)
res_l1 = sp.expand(f1(2, 2.5, 4), trig=True)

f2 = sp.lambdify((x0, x1, x2), l2)
res_l2 = sp.expand(f2(2, 2.5, 4), trig=True)
p2_x = res_l0 + res_l1 + res_l2
print("Segundo polinomio de Langrange p_2(x)\n")
print(p2_x)
#print(f"l0 = {res_l0}\nl1 = {res_l1}\nl2 = {res_l2}")
f = 1/x
fo = sp.lambdify(x, f, 'numpy')
p2_np = sp.lambdify(x, p2_x, 'numpy')

xs = np.linspace(0.1, 10, 100)
ys_f = fo(xs)
ys_pol = p2_np(xs)

plt.plot(xs, ys_f, label="f(x)=1/x", color='black')
plt.plot(xs, ys_pol,linestyle='--', label="Segundo polinomio de Langrange", color='red')
plt.draw()
input("\nPresione enter...")
plt.title("Interpolacion de lagrange para f(x)=1/x")
plt.xlabel('Eje X')
plt.ylabel('Eje Y')
plt.legend()
plt.grid()
plt.show()