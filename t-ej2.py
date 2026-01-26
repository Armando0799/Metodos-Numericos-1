#Considerar la funcion f(x) = 1/(1 + x**2) . Calcula el polinomio de cuarto orden para estimar el valor de
#f(−0.25) haciendo una tabla donde muestre el error y el numero de iteraciones. Grafiquelo
import matplotlib.pyplot as plt
import numpy as np

def taylor_f(val_x, n):
    suma = 0
    for k in range(0, n+1, 2):#pares porque la derivada impar es 0
        if k % 2 == 0:
            termino = ((-1)**(k//2)) * (val_x**k)
            suma += termino
    return suma

def f(x):
    return 1 / (1 + x**2)

x_ev = -0.25
val_real = f(x_ev)

print("="*65)
print(f"{'n':^10} | {'Aproximacion':^15} | {'Error abs':^15} | {'Error real':^15}")
print("="*65)

errores = []
grados = []
aproximaciones = []

for n in [0, 1, 2, 3, 4]:
    aprox = taylor_f(x_ev, n)
    error_abs = abs(val_real - aprox)
    error_real = error_abs / val_real

    errores.append(error_abs)
    grados.append(n)
    aproximaciones.append(aprox)
    
    print(f"{n:^10} | {aprox:^15.8f} | {error_abs:^15.8f} | {error_real:^15.8f}")

print("="*65)
print("OPERACION FINALIZADA")
print("="*65)
print(f"Valor real: {val_real}")
print(f"Valor aproximado: {aprox}")

x = np.linspace(-2, 2, 400)
y = f(x)

plt.plot(x, y, label="f(x)= 1/(1+x^2)", linewidth=2, color='black')

for n in [0, 1, 2, 3, 4]:
    y_f = taylor_f(x, n)
    plt.plot(x, y_f, label=f"Taylor de grado {n}", linewidth=2, linestyle='--')

plt.scatter([x_ev], [val_real], color='red', s=100, marker='o', zorder=5, label=f'f(-0.25)= {val_real:.4f}')
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Grafica de 1/(1+x^2) y sus polinomios de taylor")
plt.legend()
plt.grid()
#plt.ylim(-0.5, 1.5)
plt.show()