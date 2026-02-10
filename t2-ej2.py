import math
print("="*70)
#print("\t EJERCICIO 2")
print(f"| {'n':^8} | {'Aproximacion':^15} | {'Error abs':^15} | {'Valor real':^15} |")
print("="*70)

def sucesion(n):
    term = 0
    for k in range(1, n+1):
        term += 1/k
    return term - math.log(n)

val_real = 0.5772156649
tolerancia = 1e-4
n = 1

while True:
    gamma = sucesion(n)
    error_abs = abs(gamma - val_real)
    print(f"| {n:^8} | {gamma:^15.8f} | {error_abs:^15.8f} | {val_real:^15} |") #esto es opcional
    if error_abs < tolerancia:
        break
    n += 1

print("="*70)
print("\n")
print("-"*50)
print(f"El minino entero n es: {n}")
print(f"Error abs: {error_abs}")
print(f"Valor real: {val_real}")
print(f"Aproximacion: {gamma}")
print("-"*50)