#ejercicio 1.a aprox con seerie de leibniz
import math

x = 0.5
val_exacto = math.pi/4
suma = 0
n_val = []
error_relativo = []
print("="*65)
print(f"{'n':^10} | {'Aprox pi/4':^15} | {'Error abs':^15} | {'Error real':^15}")
print("="*65)

suma = 0 
for n in range(20):
    suma += (-1)**n / 2*n + 1
    error_abs = abs(val_exacto - suma)
    error_real = error_abs / val_exacto
    