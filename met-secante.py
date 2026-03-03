def f(x):
    return (x**2-1)/3
pm_1 = 0
pm = 2

for n in range(10):
    if f(pm_1) - f(pm) == 0:
        print("ERROR. Division entre cero")
        break
    
    pm1 = pm_1 - (((pm_1 - pm) * f(pm_1)) / (f(pm_1) - f(pm)))
    pm_1 = pm
    pm = pm1
    print(pm1)