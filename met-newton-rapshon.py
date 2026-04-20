import numpy as np

def f(x): #Ingresar las ecuaciones
    return np.array([x[0]**2 + x[1]**2 - 4, x[0] - x[1]])

def Mjacobino(x):
    return np.array([[2*x[0], 2*x[1]],[1, -1]]) #matriz de derivadas parciales

#puntos iniciales
x0 = np.array([np.sqrt(2), np.sqrt(2)])

for n in range(10):
    fun = f(x0)
    jacobo = Mjacobino(x0)

    delta_x = np.linalg.solve(jacobo, -fun)
    x0 += delta_x
    print(x0)