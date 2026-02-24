import math
def f(x):
    return math.sqrt(x)-math.cos(x)

a = 0
b = 1
f_a = f(a)
f_b = f(b)
iter = int(input("Ingrese el numero de iteraciones a realizar: "))
print("="*98)
print(f"| {'n':^4} | {'a':^15} | {'b':^15} | {'p_0':^15} | {'f(p_a)*f(p_0)':^15} | {"Eval en f(x)":^15} |")
print("="*98)

if f(a) * f(b) < 0:
    p0 = 0
    f_p0 = 0
    f_pa = 0
    for n in range(iter):
        p0 = (a + b)/2
        f_p0 = f(p0)
        f_pa = f(a)
        mult = f_pa * f_p0
        print(f"| {n+1:^4} | {a:^15.8f} | {b:^15.8f} | {p0:^15.8f} | {mult:^15.8f} | {f_p0:^15.8f} |")
        
        if f_p0 == 0:
            print("Estas justo en la raiz")
            break
        if f(a) * f_p0 < 0:
            b = p0
        else:
            a = p0
    print("="*98)
    print(f"\n Raiz encontada en {p0} \n")
    print(f"Evaluacion de la raiz en funcion f(x): {f_p0} \n")
else:
    print("\n")
    print("="*60)
    print("ERROR: La funcion debe de tener signos opuestos en los extremos del intervalo")
    print("="*60)