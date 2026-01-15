import math
valor_verdadero = math.exp(0.5)
tolerancia = 0.005

serie = 1
error = 1 # error grande para entrar al bucle
n = 0

print("Terminos \t Resultados \t Error relativo \t Error porcentual")

while error > tolerancia:
    valor_anterior = serie
    n = n+1
    termino = ((0.5)**n)/math.factorial(n)
    serie = serie + termino

    error_verdadero = abs(valor_verdadero - serie)
    error_porcentual = abs((serie-valor_anterior)/serie)
    error = error_porcentual

    print(f"{n} \t\t {serie:.7f} \t\t {error_verdadero:.7f} \t\t {error_porcentual:.7f}")

print(f"\nvalor verdadero: {valor_verdadero}")