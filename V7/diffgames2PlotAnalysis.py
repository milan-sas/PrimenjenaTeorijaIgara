# %% Import and Define
from math import sqrt
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt

# %% Functions

def Vfunction(current, end):
    """Function for calculating V function

    Args:
        current ([list]): List of current positions
        end ([list]): List of goals

    Returns:
        [list]: Value of V function for each player
    """    
    tmp1 = []
    tmp2 = 0
    Vi = []
    # Xi
    for index in range(len(indexes)):
        # Xj
        tmp1 = []
        for cnt in range(len(indexes)):
            # i > j
            if cnt != index:
                # Find value
                # || Xi - Xj ||
                xi = norm(current[index] - current[cnt])
                tmp2 = (R**2 - xi**2) / (xi**2 - r**2)
                # max{tmp2, 0}
                if tmp2 < 0:
                    tmp2 = 0
                else: pass
            else: tmp2 = 0
            tmp1.append(tmp2**2)
            tmp2 = 0
        # || Xi - Zi ||
        xi = norm(current[index] - end[index])
        Vi.append([1/2*(xi)**2 + 1/2*i for i in tmp1])

    return Vi

def Vderative(current, end):
    """Function for calculatig derative of V function

    Args:
        current ([list]): List of current positions
        end ([list]): List of goals

    Returns:
        [list]: Derative value of V function for each player
    """    
    tmp1 = []
    tmp2 = 0
    Vi = []
    # Xi
    for index in range(len(indexes)):
        # Xj
        tmp1 = []
        for cnt in range(len(indexes)):
            # i > j
            if cnt != index:
                # Find value
                # || Xi - Xj ||
                xi = norm(current[index] - current[cnt])
                # tmp2 = (2*(R**2 - xi**2)*(-2*R**2 *xi+2*xi*r**2)) / (xi**2 - r**2)**3
                tmp2 = (4*xi*(r**2 - R**2)*(R**2-xi**2)) / (xi**2-r**2)
                # max{tmp2, 0}
                if tmp2 < 0:
                    tmp2 = 0
                else: pass
            else: tmp2 = 0
            tmp1.append(tmp2)
            tmp2 = 0
        # || Xi - Zi ||
        xi = norm(current[index] - end[index])
        Vi.append([xi + i for i in tmp1])
    return Vi

def speed(a, current, end):
    """Function for calculatinf speed vector

    Args:
        a ([list]): List of derative values of V function for each player
        current ([list]): List of current positions
        end ([list]): List of goals

    Returns:
        [list]: Speed vector for each player
    """    
    v = []
    for i in range(len(indexes)):
        tmp = 0
        for j in range(len(indexes)):
            if j>i:
                # Sum aij* (Xi - Xj)
                tmp += 1/a[i][j]*(current[i] - current[j])
            else:
                pass

        # Zi - Xi + sum
        tmp += end[i] - current[i]
        v.append(tmp/norm(tmp))
    return v

def newState(current, u):
    """Calculates new position for each player

    Args:
        current ([list]): List of current positions
        u ([list]): List of speed vectors for each player

    Returns:
        [list]: New positions for each player
    """    
    r = []
    for ind in indexes:
        r.append(np.add(current[ind], u[ind]))
    return r


# %% Main

# 3 independent flying objects
# one point (x,y)
startingPoint = [np.asarray((5,0)), np.asarray((10,10)), np.asarray((15,0))]
endingPoint = [np.asarray((12,5)), np.asarray((5,5)), np.asarray((5,10))]
indexes = [0,1,2]
# Max speed (speed vector length)
Vmax = 1
# Radius of detection
R = 2
# Collision distance
r = 1
# Current position
currentState = [[],[],[]]
# History of positions
history = [[], [], []]

currentState[0] = startingPoint[0]
currentState[1] = startingPoint[1]
currentState[2] = startingPoint[2]

# History for first object
history[0].append(startingPoint[0])
# History for second object
history[1].append(startingPoint[1])
# History for third object
history[2].append(startingPoint[2])

Vcurrent = [None]*len(indexes)
Speed = [None]*len(indexes)

# while True:
for i in range(20):
    Vcurrent = np.array(Vfunction(currentState, endingPoint))
    # print(Vcurrent)
    # print('--------------------')
    Vder =  np.array(Vderative(currentState, endingPoint))
    # print(Vder)
    # print('--------------------')
    Speed = Vmax * np.asarray(speed(Vder, currentState, endingPoint))
    # print(Speed)
    # print('--------------------')
    currentState = newState(currentState, Speed)
    # print(currentState)
    # print("Number of iterations: " + str(i))
    # History for first object
    history[0].append(currentState[0])
    # History for second object
    history[1].append(currentState[1])
    # History for third object
    history[2].append(currentState[2])
    # If object have reached close enough to the final point
    if norm(currentState[0]-endingPoint[0])<1 and norm(currentState[1]-endingPoint[1])<1 and norm(currentState[2]-endingPoint[2])<1:
        break

# %% Ploting history

#print(history)

X1 = history[0]
X2 = history[1]
X3 = history[2]

# print("----------")
# print(X1)
# print("----------")
# print(X2)
# print("----------")
# print(X3)
# print("----------")

xVal = [x[0] for x in X1]
yVal = [x[1] for x in X1]
plt.plot(xVal, yVal, 'ro', label="X1")
i = 0
for x,y in zip(xVal, yVal):
    plt.annotate(i, (x,y),textcoords="offset points", xytext=(0,5), ha='center')
    i += 1

plt.legend()
plt.grid()
#plt.show()

xVal = [x[0] for x in X2]
yVal = [x[1] for x in X2]
plt.plot(xVal, yVal, 'bo', label="X2")
i = 0
for x,y in zip(xVal, yVal):
    plt.annotate(i, (x,y),textcoords="offset points", xytext=(0,5), ha='center')
    i += 1
plt.legend()
plt.grid()
#plt.show()

xVal = [x[0] for x in X3]
yVal = [x[1] for x in X3]
plt.plot(xVal, yVal, 'go', label="X3")
i = 0
for x,y in zip(xVal, yVal):
    plt.annotate(i, (x,y),textcoords="offset points", xytext=(0,5), ha='center')
    i += 1
plt.legend()
plt.grid()
#plt.show()

# Print final position
for i in range(len(indexes)):
    print("Object {} projected final position: ".format(i+1) + str(endingPoint[i]))
    print("Object {} real final position: ".format(i+1) + str(history[i][-1]))


# %%
