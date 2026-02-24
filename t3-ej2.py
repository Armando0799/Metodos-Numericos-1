#ejercicio 2 del metodo de biseccion
def f(x):
    return 2*x**3-x**2+x-1

iter = int(input("Ingres el numero de iteraciones a realizar: "))
print("="*98)
print(f"| {'n':^4} | {'a':^15} | {'b':^15} | {'p_0':^15} | {'f(p_a)*f(p_0)':^15} | {'Eval en f(x)':^15} |")
print("="*98)
a = 0
b = 1
f_a = f(a)
f_b = f(b)

if f_a * f_b < 0:
    p0 = 0
    f_p0 = 0
    f_pa = 0
    for n in range(iter):
        p0 = (a + b)/2
        f_p0 = f(p0)
        f_pa = f(a)
        mult = f_pa * f_p0
        print(f"| {n+1:^4} | {a:^15.8f} | {b:^15.8f} | {p0:^15.8f} | {mult:^15.8f} | {f_p0:^15.8} |")

        if f_p0 == 0:
            break
        if f(a) * f_p0 < 0:
            b = p0
        else:
            a = p0
    print("="*98)
    print(f"Raiz encontrada en: {p0} \n")
    print(f"Evaluacion de la raiz en la funcion f(x): {f_p0} \n") #Esto puede ser opcional
else:
    print("\n")
    print("="*60)
    print("Error: la funcion debe de tener signos opuestos en los extremos del intervalo.")
    print("="*60)