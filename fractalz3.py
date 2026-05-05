import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
def f(z):
    return z**3 - 1

def df(z):
    return 3*z**2

def newton(z0, tol=1e-6, max_iter=50):
    z = z0
    for i in range(max_iter):
        if abs(df(z)) < 1e-12:
            break
        z = z - f(z)/df(z)
        if abs(f(z)) < tol:
            break
        #print(f"Iteracion {i+1}: z = {z}") aca esto puede ser opcional ya que imprime
        #muchos resultados y eso es muy estresante en la terminal
    return z

r = np.array([
    1 + 0j,
    -0.5 + np.sqrt(3)/2 * 1j,
    -0.5 - np.sqrt(3)/2 * 1j
])

def clasifica(z):
    distancia = [abs(z - r) for r in r]
    return np.argmin(distancia)

N = 400
x = np.linspace(-2, 2, N)
y = np.linspace(-2, 2, N)

resultado = np.zeros((N, N))

for i in range(N):
    for j in range(N):
        z0 = x[i] + 1j*y[j]
        z_final = newton(z0)
        resultado[j, i] = clasifica(z_final)
cmap = ListedColormap(['green', 'white', 'red'])
plt.figure(figsize=(6,6))
plt.imshow(resultado, extent=(-2,2,-2,2), cmap=cmap)
plt.title("Funcion de $z^3 - 1$")
plt.xlabel("Re(z)")
plt.ylabel("Im(z)")
plt.colorbar(label="Raíz alcanzada")# barra alado de la grafica con el color del los resultados
plt.show()