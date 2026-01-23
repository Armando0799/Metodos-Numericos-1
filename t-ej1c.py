#aproximacion de pi mediante la serie de ramanuyan
import math
val_exacto = math.pi
print("="*68)
print(f"{'n':^10} | {'Aprox 1/pi':^14} | {'Error abs':^17} | {'Error real':^14}")
print("="*68)

suma = 0
for n in range(500):
    termino = (math.factorial(4*n) * (1103 + 26340 * n))/((math.factorial(n))**4 * 396**(4*n))
    suma += termino
    aprox_pi = 9801 / (2*math.sqrt(2)* suma)
    error_abs = abs(val_exacto - aprox_pi)
    error_real = error_abs / val_exacto
    
    print(f"{n:^10} | {aprox_pi:^14.12} | {error_abs:^14.10} | {error_real:^14.10}")
    
    if error_real < 0.5e-8:
        print(f"\nCoincidencia encontrada en: {n}")
        break

print("*"*50)
print("\n OPERACION FINALIZADA\n")
print("*"*50)
print(f"Valor real de 1/pi: {val_exacto}")
print(f"Valor aproximado: {aprox_pi}")
