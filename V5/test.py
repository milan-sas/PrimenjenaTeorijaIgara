# %% Define
x = 0.42857
y = 0.2


u1 = -5*(1-x)*y + 15*x*y - 3*x*(1-y) + 2*(1-x)*(1-y)
u2 = 15*y*(1-x) - 20*x*y 

print("Guard: " + str(u1))
print("Thieve: " + str(u2))

# %%

print(-5*(1-x)*y) 
print(15*x*y)
print(3*x*(1-y))
# %% Define
import sympy as sym

N,Z,P,B,C,S = sym.symbols('N,Z,P,B,C,S')
x,y = sym.symbols('x,y')

Uc = N*x*y - P*(1-x)*y - C*x*(1-y) + S*(1-x)*(1-y)
Ul = -Z*x*y + B*(1-x)*y

print("Uc : {}".format(Uc))
print("Ul : {}".format(Ul))

dUcdx = sym.Derivative(Uc,x).doit()
dUldy = sym.Derivative(Ul,y).doit()

print("dUcdx : {}".format(dUcdx))
print("dUldy : {}".format(dUldy))

du1 = sym.Eq((dUcdx), 0)
du2 = sym.Eq((dUldy), 0)

print("dUc : {}".format(du1))
print("dUl : {}".format(du2))

x,y = sym.nsolve((du1, du2), (x,y), (1,1))

print("Player 1 equilibrium : " + str(x))
print("Player 2 equilibrium : " + str(y))

# %%
