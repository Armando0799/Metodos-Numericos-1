def g(x):
    return 2/x

p0 = 1
for n in range(10):
    pm = g(p0)
    p0 = pm
    print(f"p_{n+1} = {p0}")
print("Observemos que la sucesion g(x) oscila entre 1 y 2 por lo tanto la sucesion diverge\n")