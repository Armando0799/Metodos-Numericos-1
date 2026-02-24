import math
print("Ingrese el intervalo [a, b]")
a = int(input("Ingrese el valor de a: "))
b = int(input("Ingrese el valor de b: "))
fun = input("Ingrese la funcion f(x): ")
iter = int(input("Ingrese el numero de iteraciones a realizar: "))
print("="*98)
print(f"| {'n':^4} | {'a':^15} | {'b':^15} | {'p0':^15} | {'f(p_a)*f(p_0)':^15} | {'Eval en f(x)':^15} |")
print("="*98)

def f(x):
    reemplazo = fun.replace('x', str(x))
    evaluacion = eval(reemplazo)
    return evaluacion

f_a = f(a)
f_b = f(b)
if f_a * f_b < 0:
    p0 = 0
    f_p0 = 0
    f_pa = 0
    for n in range(iter):
        p0 = (a + b) / 2
        f_p0 = f(p0)
        f_pa = f(a)
        mult = f_pa * f_p0
        print(f"| {n+1:^4} | {a:^15.8f} | {b:^15.8f} | {p0:^15.8f} | {mult:^15.8f} | {f_p0:15.8f} |")

        if f_p0 == 0:
            print("Estas justo en la raiz")
            break
        if f(a) * f_p0 < 0:
            b = p0
        else:
            a = p0
    print("="*98)
    print(f"\n Raiz encontra en {p0}")
    print(f"\n Evaluacion de la raiz en la funcion f(x): {f_p0} \n")

else:
    print("\n")
    print("="*60)
    print("ERROR: La funcion debe de tener signos opuestos en los intervalos.")
    print("="*60)