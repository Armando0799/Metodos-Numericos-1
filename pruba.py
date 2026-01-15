import math

valor_verdadero = math.exp(0.5)
tolerancia = 0.005

# Corrección 1: Inicializar correctamente
serie = 1  # Término n=0: x^0/0! = 1
n = 0  # Empezamos desde n=0
error = 1  # Error inicial grande para entrar al bucle

print("Términos\tAproximación\tError Verdadero\tError Relativo")
print("-" * 60)

# Corrección 2: Condición del bucle
while error > tolerancia:
    valor_anterior = serie
    n = n + 1
    # Corrección 3: Sumar el término correcto (n actual)
    termino = ((0.5)**n) / math.factorial(n)
    serie = serie + termino
    
    # Corrección 4: Calcular errores correctamente
    error_verdadero = abs(valor_verdadero - serie)
    error_relativo = abs((serie - valor_anterior) / serie)  # Usar valor actual, no anterior
    
    # Usamos el error relativo para la condición
    error = error_relativo
    
    print(f"{n}\t\t{serie:.6f}\t\t{error_verdadero:.6f}\t\t{error_relativo:.6f}")

print("\n" + "=" * 60)
print(f"Valor verdadero: {valor_verdadero:.6f}")
print(f"Aproximación final: {serie:.6f}")
print(f"Número de términos necesarios: {n}")
print(f"Error absoluto final: {abs(valor_verdadero - serie):.6f}")