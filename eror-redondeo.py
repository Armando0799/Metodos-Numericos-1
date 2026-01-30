import matplotlib.pyplot as plt
import numpy as np

m = np.linspace(0, 15, 200)
error = 0.3334e-4*m

plt.figure()
plt.plot(m, error)
plt.xlabel("m")
plt.ylabel(r"$p_m-\hat{p}_m$")
plt.title("Grafica de error por redondeo")
plt.grid()
plt.show()