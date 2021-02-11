
# %%
import matplotlib.pyplot as plt

# payoffs 
V = 10 
C = 30

xG = [0.02]
xS = [1 - xG[0]]
dt = 0.05
# utility functions of hawk and dove
UG = [(xG[0] * V/2 + xS[0] * 0) * dt]
US = [(xG[0] * V + xS[0] * (V-C)/2) * dt]
# average utility
UAvg = [(xG[0] * UG[0] + xS[0] * US[0]) * dt]


for t in range(40):
    # utilities
    uG = (xG[t] * V/2 + xS[t] * 0) 
    uS = (xG[t] * V + xS[t] * (V-C)/2) 
    uAvg = (xG[t] * uG + xS[t] * uS)
    UG.append(uG*dt)
    US.append(uS*dt)
    UAvg.append(uAvg*dt)
    # differential equations
    xG.append(xG[t] + (xG[t] * (uG - uAvg)) * dt)
    xS.append(xS[t] + (xS[t] * (uS - uAvg)) * dt)

plt.plot(xG, 'r', label ='population of doves')
plt.plot(xS, 'b', label ='population of hawks')
plt.grid()
plt.ylim(0, 1)
plt.legend(loc='best')

# %%