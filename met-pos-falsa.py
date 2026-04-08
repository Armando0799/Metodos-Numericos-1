import math
def f(x):
    return math.exp(3*x)-4 #x**3-3*x+1

print("Ingrese el intervalo (a, b):")
a = float(input("Ingrese el valor de a: "))
b = float(input("Ingrese el valor de b: "))

print("="*60)
print(f"{'n':^3} | {'a_n':^10} | {'b_n':^10} | {'p_n':^10} | {'f(p_n)':^10}")
print("="*60)

if f(a) * f(b) < 0:
    for n in range(10):
        x_i = (a * f(b) - b * f(a)) / (f(b) - f(a))

        print(f"{n:^3} | {a:^8.8f} | {b:^8.8f} | {x_i:^8.8f} | {f(x_i):^8.8f}")

        if f(a) * f(x_i) < 0:
            b = x_i
        else:
            a = x_i
    print("="*60)
    print(f"Raiz obtenida despues de {n+1} iteraciones: {x_i}")
else:
    print("Error. La funcion debe de tener signos distintos al evaluarlo en los extremos")