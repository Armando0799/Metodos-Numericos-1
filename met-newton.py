import math
p0 = float(input("Ingrese el punto inicial: "))
#faltan pequños arrreglos.
#fun = input("Ingrese la funcion: ")
#funp = input("Ingrese la primera derivada de la funcion: ")
iter = int(input("Ingrese el numero de iteraciones a realizar: "))

"""def f_val(x):
    reem = fun.replace('x', str(x))
    evaluar = eval(reem)
    return evaluar"""

def f(x):
    return (x**2 - 1) / 3

"""def fp_val(x):
    reem = funp.replace('x', str(x))
    evaluar = eval(reem)
    return evaluar"""

def fp(x):
    return (2/3)*x

for n in range(iter):
    pm = p0 - (f(p0)/fp(p0))
    p0 = pm
    print(pm)