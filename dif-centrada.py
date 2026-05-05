import sympy as sp
import matplotlib.pyplot as plt

def f(x):
    return -0.1*x**4-0.15*x**3-0.5*x**2-0.25*x+1.2

t_i = 0.5
t_i1 = 0.75
t_i2 = 1
h = 0.25

fp = (4*(f(t_i1)) -3*(f(t_i)) -f(t_i2))/(2*(h))
print(f"La derivada aproximacion es: {fp}\n")
x = sp.symbols('x')
derivada = sp.diff(f(x), x)
print(f"La drtivada de la funcion es: {derivada}\n")

fi = sp.lambdify(x, derivada)
print(f"La derivada real evaluada en 0.5 es: {fi(0.5)}\n")
e = abs((fi(0.5)-fp)/fi(0.5))*100
print(f"El error es del {e}%")

def aprox(x, h):
    return(4*(f(x+h))-3*(f(x))-f(x+2*h))/(2*(h))

h_val = [0.5, 0.25, 0.125, 0.0625, 0.03125]
errores = []

for n in h_val:
    fp1 = aprox(t_i, n)
    error = abs((-0.9125-fp1)/-0.9125)
    errores.append(error)

plt.plot(h_val, errores, color ='red')
plt.draw()
plt.title("Grafica de errores")
#plt.xscale('log')
#plt.yscale('log')
plt.xlabel('Eje x')
plt.ylabel('Eje y')
plt.grid()
plt.show()