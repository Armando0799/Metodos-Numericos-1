import math as mt
print("="*70)
print(f"| {'n':^5} | {'Aproximacion':^15} | {'Error abs':^15} | {'Valor real':^15} |")
print("="*70)

x = 0.5
val_real = mt.exp(x)

def taylor_exp(x, tole=1e-3):
    sum = 0
    term = 1
    k = 0
    while term >= tole:
        sum += term
        k += 1
        term = x**k/mt.factorial(k)
    return sum, k

def taylor_exp1(k, n):
    sum = 0
    tol = 1e-3
    for k in range(n+1):
        term = sum + x**k/mt.factorial(k)
        sum += term
        if term >= tol:
            print(f"Aproximacion encontrada en n = {k+1}")
            break