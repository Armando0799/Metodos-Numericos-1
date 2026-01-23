"""realiza una tabla donde muestre el error y el numero de iteraciones para aproximarse al valor de \sqrt{2} 
con cinco cifras significativas con el polinomio de Taylor de f(x) =\sqrt{1 + x} cerca del punto 1/2"""
import math

val_exacto = math.sqrt(2)
a = 1/2
x = 1
e_n = (x - a)
print("="*65)
print(f"{'n':^10} | {'Aprox \sqrt(2)':^14} | {'Error abs':^14} | {'Error real':^14}")
print("="*65)

suma = 0
coeficientes = 1

for n in range(150):
    if n == 0:
        termino = math.sqrt(1 + a)
    else:
        coeficientes = -(2*n - 3) / (2*n)
        termino = (coeficientes * (e_n)**n) / math.factorial(n)
    suma += termino

    error_abs = abs(val_exacto - suma)
    error_real = error_abs / val_exacto

    #if n <= 20 or n % 1000 == 0:
    print(f"{n:^10} | {suma:^14.8f} | {error_abs:^14.8f} | {error_real:^14.8f}")
    

    if suma < 0.5e-3:
        print(f"Coincidencia encontrada en {n}")
        break

print("*"*40)
print(f"Valor real de sqrt(2): {val_exacto}")
print(f"Valor aproximado: {suma}")
