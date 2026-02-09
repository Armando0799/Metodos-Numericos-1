import math as mt
print("="*63)
print(f"| {'n':^5} | {'Aproximacion':^15} | {'Error abs':^15} | {'Valor real':^15} |")
print("="*63)

def taylor_exp(x, tole=1e-3):
    sum = 0
    term = 1
    k = 0
    while term >= tole:
        sum += term
        k += 1
        term = x**k/mt.factorial(k)
        error = abs(val_real - sum)
        print(f"| {k:^5} | {sum:^15.8f} | {error:^15.8f} | {val_real:^15.8f} |")
    return sum, k, error

x = 0.5
val_real = mt.exp(x)
tol = 1e-3

aprox, num_i, error_abs = taylor_exp(x, tol)

print("="*63)
print("\n")
print("-"*50)
print(f"Valor real: {val_real}")
print(f"Aproximacion: {aprox}")
print(f"Aproximacion encontrada en: {num_i}")
print("-"*50)