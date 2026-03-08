import math
# funcion obtenida al despejar x
def g(x):
    return math.sqrt(10/(x+4))
#funcion dada en el ununciado
def ev(x):
    return x**3+4*x**2-10

i = int(input("Ingrese el numero de iteraciones a realizar: "))
print("="*55)
print(f"| {'n':^4} | {'p0':^8} | {'Aproximacion':^15} | {'Evalua en f(x)':^15} |")
print("="*55)
p0 = 1.5
for n in range(i):
    pm = g(p0)# obtiene la aproximacion
    p0 = pm
    e = ev(pm)# evalua en la funcion dada
    print(f"| {n+1:^4} | {p0:^8.5f} | {pm:^15.10f} | {e:^15.10f} |")
print("="*55)