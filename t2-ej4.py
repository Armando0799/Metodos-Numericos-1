import math
print("="*65)
print("\t EJERCICIO 4")
print("="*65)

def p_9(x):
    sum = 0
    for n in range(10):
        sum += (x**n)/math.factorial(n)
    return sum

cota = math.e / math.factorial(10)
tol = 1e-6
max_error = 0
max_error_x = 0
num_p = 101

for i in range(num_p):
    x = -1 + 2 * i / (num_p - 1)
    val_exacto = math.exp(x)
    aprox = p_9(x)
    error_abs = abs(val_exacto - aprox)
    if error_abs > max_error:
        max_error = error_abs
        max_error_x = x

"""print("-"*65)
print("Verificacion del error maximo para x en [-1, 1]")
print(f"e: {math.e}")
print(f"10!: {math.factorial(10)}")
print(f"Cota teorica del error e/10!= {cota}")
print("-"*65)
print("\n")"""
print("-"*65)
print(f"Verificacion numerica en {num_p} puntos para x en [-1, 1]")
print(f"Maximo error encontrado en {max_error} en x= {max_error_x}")
print("-"*65)
print("Comparacion con la cota teorica")
print(f"Cota teorica: {cota}")
print(f"Error maximo (|e^x - p_9(x)|): {max_error}")
print("-"*65)

if cota <= tol and max_error <= tol:
    print("Por lo tanto si se cumple que |e^x - p_9(x)|<= 10^-6 para toda x en [-1, 1]")
    print("Ya que la cota teorica es menor que 10^-6\n i, e. |e^x - p_9(x)| <= 7.49e-7 < 10^-6")
    print("="*65)
else:
    print("Por lo tanto no se cumple la condicion")