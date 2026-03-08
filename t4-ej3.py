def f(x):
    return (x**2-1)/3

def g(x):
    return 1

iter = int(input("Ingrese el numero de iteraciones a realizar: "))
print("="*50)
print(f"| {'n':^4} | {'Aproximacion':^15} | {'Evalua en f(x)':^15} |")
print("="*50)
x0 = 0
for n in range(iter):
    pm = f(x0)
    e = f(pm)
    x0 = pm
    print(f"| {n+1:^4} | {pm:^15.10f} | {e:15.10f} |")
print("="*50)