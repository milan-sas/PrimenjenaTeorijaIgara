# %% Import and Deffinitions
import sympy as sym

dx, x, d, c, v = sym.symbols('dx,x,d,c,v')
x = (c-v)/c
dx = 3/2*c*d*x**2 - 2*c*d*x + c/2*d + c/2*x**3 - c*x**2 + c/2*x + v*d*x - v/2*d + v/2*x**2 - v/2*x

print("Utility 1 : {}".format(dx))


print('---------------------------')
# %%