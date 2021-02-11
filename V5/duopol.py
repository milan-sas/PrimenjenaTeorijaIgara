# %% Import and Deffinitions
import sympy as sym

a1, a2 = sym.symbols('a1,a2')
# Costs
c1 = 5000/a1
c2 = 3000/a2
# Price structure
p = 100-(a1+a2)
# Utility for players
u1 = p*a1 - c1
u2 = p*a2 - c2

print("Utility 1 : {}".format(u1))
print("Utility 2 : {}".format(u2))
print('---------------------------')

# dU1/da1   aU2/da2
duda1 = sym.Derivative(u1,a1).doit()
duda2 = sym.Derivative(u2,a2).doit()

print("du1/da1 : {}".format(duda1))
print("du2/da2 : {}".format(duda2))
print('---------------------------')

# dU1/da1=0   aU2/da2=0
du1 = sym.Eq((duda1), 0)
du2 = sym.Eq((duda2), 0)

# Soving system
a1,a2 = sym.nsolve((du1, du2), (a1,a2), (100,100))

# Results
print("Player 1 equilibrium : " + str(a1))
print("Player 2 equilibrium : " + str(a2))

# Unit price
p = 100-(a1+a2)

print("Unit price: "+ str(p))

# Utility for players
u1 = p*a1 - 5000/a1
u2 = p*a2 - 3000/a2

print("Player 1 utility : " + str(u1))
print("Player 2 utility : " + str(u2))

print('---------------------------')
# %%