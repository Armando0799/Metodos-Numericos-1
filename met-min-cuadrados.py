import numpy as np
import matplotlib.pyplot as plt

xi = np.array([8.87, 8.29, 8.49, 8.75, 8.86,
    9.23, 10.75, 10.00, 10.15, 10.01])

yi = np.array([0.31, -0.13, -0.06, -0.31,
    0.35, 0.20, 1.80, 0.57, 1.11, 1.61])

n = len(xi)
sx = np.sum(xi)
sy = np.sum(yi)
sxy = np.sum(xi * yi)
sxx = np.sum(xi * xi)
# Calculo de la pendiente
m = (n*sxy - sx*sy)/(n*sxx - sx**2)
print(m)
# Calculo de b
b = (sy - m*sx)/n
print(b)
# recta
recta = b + m * xi

plt.figure()
plt.scatter(xi, yi, color='red')
plt.plot(xi, recta, color='black')
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Grafica con minimos cuadrados")
plt.grid()
plt.show()