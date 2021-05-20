import numpy as np
import matplotlib.pyplot as plt

### Define
w = np.pi/4

### inv_DFT()
inv_DFT = lambda t: np.sin(w*t)/(t*np.pi)

### Main
n = np.arange(-15, 16, 0.5)
x_n = inv_DFT(n)
x_n[np.isnan(x_n)] = w/np.pi # Converts NaN to the l'hopital value

### Plot
plt.stem(n, x_n)
plt.title("W = π/4")
plt.show()
