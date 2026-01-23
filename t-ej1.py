#ejercicio 1.a aprox con seerie de leibniz
import math

val_exacto = math.pi
print("="*65)
print(f"{'n':^10} | {'Aprox pi/4':^15} | {'Error abs':^15} | {'Error real':^15}")
print("="*65)

suma = 0 
for n in range(0, 2000000000):
    termino = (-1)**n / (2*n + 1)
    suma +=  termino
    aprox_pi = 4 * suma

    error_abs = abs(val_exacto - aprox_pi)
    error_real = error_abs / val_exacto

    if n <= 20 or n % 1000000 == 0:#imprime los primeros 10 y despues cada 1000
        print(f"{n:^10} | {aprox_pi:^15.10f} | {error_abs:^15.10f} | {error_real:^14.10f}")
    
    if error_real < 0.5e-8:
        print(f"\n Presicion encontrada en n = {n}")
        break

print("="*65)
print("\n RESULTADO FINAL (resumido)")
print(f"Valor exacto: {val_exacto:.15f}")
print(f"Valor aproximado: {aprox_pi:.15f}")
