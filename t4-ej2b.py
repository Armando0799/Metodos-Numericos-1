#ejercicio 2 b 
import math
def g(x):
    return (1/2)*(x + math.cos(x))

p0 = 2
for n in range(15):
    pm = g(p0)
    p0 = pm
    print(f"p_{n+1} = {p0}")
print("Por lo tanto la sucesion converge\n")