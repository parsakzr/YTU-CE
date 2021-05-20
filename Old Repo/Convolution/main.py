import numpy as np
import matplotlib.pyplot as plt

# --- myConv ---
def myConv(x, h):
    # returns the convolution of two discrete finite vectors
    # = x*h[n] = sum( x[n]h[m-n])

    M, N = len(x), len(h) # Multiple uses
    
    if M>N: # Extend h
        h = np.append(h, np.zeros(M-N))
    elif M<N: # Extend x
        x = np.append(x, np.zeros(N-M))

    y = np.zeros(2*M-1) # Will be the right size before returning

    for n in range(M): # n : 0->M
        for k in range(n+1):
            y[n] += x[k] * h[n-k]

    for n in range(M, 2*M-1): # n : M->End
        for k in range(n+1):
            if k < M and n-k < M: # Filtering the out of bounds
                y[n] += x[k] * h[n-k]

    y = y[:M+N-1] # remove the Extra 0

    return y

''' Without Extending ( Only works if M==N)
    M, N = len(x), len(h) # Multiple uses

    y = np.zeros(M+N-1) # 

    for n in range(M): # n: 0->M
        for k in range(n+1.
            y[n] += x[k] * h[n-k]

    for n in range(M, M+N-1): # n: M->End
        for k in range(n+1):
            if k < M and n-k < N: # Filtering the out of bounds
                y[n] += x[k] * h[n-k]

    return y
'''

def gen_ny(nx, nh):
    ny = np.arange(nx[0]+nh[0], nx[-1]+nh[-1] + 1)
    return ny

# --- definition ----
nx = np.arange(1, 11)
x = 2**nx

nh = np.arange(-2, 3)
h = nh*2

ny = gen_ny(nx, nh)
y = np.convolve(x, h)
my_y = myConv(x, h)

print("x= ", x)
print("h= ", h)
print("-"*40)
print("   y = ", y)
print("-"*20)
print("my_y = ", my_y)

# --- Plot ---
fig, plots = plt.subplots(2, 2)
fig.suptitle("Convolution")

plots[0, 0].scatter(nx, x)
plots[0, 0].set_title("x[n]")

plots[0, 1].scatter(nh, h)
plots[0, 1].set_title("h[n]")

plots[1, 0].scatter(ny, my_y)
plots[1, 0].set_title("my_y[n]")

plots[1, 1].scatter(ny, y)
plots[1, 1].set_title("y[n]")

plt.show()
