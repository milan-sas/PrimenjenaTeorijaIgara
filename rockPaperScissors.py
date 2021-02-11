# %%
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(15,5))
fig.add_subplot(1,2,1)

xR = [0.3]
xP = [0.3]
xS = [1-xR[0]-xP[0]]
dt = 0.001

for t in range(50000):
    # oscillations
    uR = xR[t] * 0 + xP[t] * -1 + xS[t] * 1
    uP = xR[t] * 1 + xP[t] * 0 + xS[t] * -1
    uS = xR[t] * -1 + xP[t] * 1 + xS[t] * 0
    uAvg = xR[t] * uR + xP[t] * uP + xS[t] * uS
    xR.append(xR[t] + (xR[t] * (uR - uAvg)) * dt)
    xP.append(xP[t] + (xP[t] * (uP - uAvg)) * dt)
    xS.append(xS[t] + (xS[t] * (uS - uAvg)) * dt)

plt.plot(xR, 'g', label = 'rock')
plt.plot(xP, 'b', label = 'paper')
plt.plot(xS, 'r', label = 'scissors')
plt.title('Replicator dynamics of the"Rock, paper, scissors"-game')
plt.legend(loc='best')
plt.grid()

fig.add_subplot(1,2,2)
plt.plot(xR, xS)
plt.title('Phase space of the"Rock, paper, scissors"-game')
plt.xlabel('rock')
plt.ylabel('scissors')
plt.grid()

# %%