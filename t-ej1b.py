#aproximacion de pi mediante serie de taylor de arctan(x) en 0
import math

val_exacto = math.pi
print("="*65)
print(f"{'n':^10} | {'Aprox pi':^14} | {'Error abs':^14} | {'Error real':^14}")
print("="*65)
suma = 0

for n in range(10000000):
    x = 1
    termino = ((-1)**n * x**(2*n+1)) / (2 * n+1)
    suma += termino
    aprox_pi = 4 * suma
    error_abs = abs(val_exacto - aprox_pi)
    error_real = error_abs / val_exacto
    
    if n <= 20 or n % 1000 == 0:
        print(f"{n:^10} | {aprox_pi:^14.11f} | {error_abs:^14.11f} | {error_real:^14.11f}")

    if error_real < 0.5e-8:
        print(f"Coincidencia encontrada en {n}")
        break

print(f"Valor real de pi: {val_exacto}")
print(f"Valor aproximado: {aprox_pi}")
