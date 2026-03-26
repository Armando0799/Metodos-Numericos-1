import math

def f(x):
    return math.exp(-x)-x

p0 = 0
p1 = 1
print("="*40)
print(f" {'n':^5} | {'p_n':^10} | {'f(p_n)':^10} ")
print("="*40)

for n in range(10):
    if f(p0) - f(p1) == 0:
        print("="*40)
        print("ERROR. Division entre cero")
        break

    p_n1 = p1 - ((f(p1)*(p1 - p0)) / (f(p1) - f(p0)))
    print(f" {n+1:^5} | {p0:^10.10f} | {f(p_n1):^10.10f} ")
    p1 = p0
    p0 = p_n1