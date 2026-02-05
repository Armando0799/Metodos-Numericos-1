print("Ingrese el intervalo [a, b] ")
a = float(input("Ingrese el valor de (a): "))
b = float(input("Ingrese el valor de (b): "))
f = input("Ingrese la funcion: ")
r = input("Ingrese el valor de la tolerancia: ")
r_string = eval(r)

def eval_f(x_val):
    reemplazo = f.replace('x', str(x_val))
    evaluacion = eval(reemplazo)
    return evaluacion

f_a = eval_f(a)
f_b = eval_f(b)

if f_a * f_b < 0:
    p_1 = 0
    while b - a > r_string:
        p_1 = (a + b)/2
        f_p1 = eval_f(p_1)

        if f_p1 == 0:
            break

        if eval_f(a) * f_p1 < 0:
            b = p_1
        else:
            a = p_1
    print(f"Raiz encontrada en: {p_1}")
else:
    print("\n*"*35)
    print("ERROR: La funcion debe de tener signos opuestos en los extremos del intervalo.")