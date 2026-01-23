import matplotlib.pyplot as plt
import numpy as np

def taylor_ln(x, n):
    suma = 0
    for k in range(1, n + 1):  # k va de 1 a n
        term = ((-1) ** (k + 1)) * (x - 1) ** k / k
        suma += term
    return suma

x = np.linspace(0.1, 2, 400)

plt.figure(figsize=(8, 6))
plt.plot(x, np.log(x), label=r"$\ln(x)$", linewidth=2, color='black')

for n in [1, 2, 4, 8, 16]:
    y_taylor = taylor_ln(x, n)
    plt.plot(x, y_taylor, label=f"Taylor grado {n}", linewidth=1)

plt.xlabel("x")
plt.ylabel("y")
plt.title(r"Aproximaciones de Taylor de $\ln(x)$ alrededor de $x=1$")
plt.legend()
plt.grid()
plt.show()
