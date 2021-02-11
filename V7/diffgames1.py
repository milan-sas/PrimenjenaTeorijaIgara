# %% Import and define
from math import sqrt, atan, cos, sin
import numpy as np
import matplotlib.pyplot as plt

# 3 independent flying objects
# one point (x,y)
startingPoint = [(5,0), (10,0), (15,0)]
endingPoint = [(10,10), (15,10), (5,10)]
indexes = [0,1,2]
# Max speed (speed vector length)
Vmax = 1
# Safe zone around object
safeDistance = 1
# Current cpeed for reach object, represented as x and y components of speed vector
currentSpeed = [[None, None], [None, None], [None, None]]
# Current linear equation (path from start to end)
currentEq = [[], [], []]
# Current position
currentState = [[],[],[]]
# History of positions
history = [[], [], []]
# Objects with lower ID shoud stop
hold = [False, False, False]
# Objects with higher ID shoud evade
getReadyToEvade = [False, False, False]
# Object is in final point
reachedEnd = [False, False, False]

currentState[0] = startingPoint[0]
currentState[1] = startingPoint[1]
currentState[2] = startingPoint[2]

# History for first object
history[0].append(startingPoint[0])
# History for second object
history[1].append(startingPoint[1])
# History for third object
history[2].append(startingPoint[2])

# %% Functions
# Trajectory equation 
def trajectory(start, end):
    """Calculates linear trajectory of object

    Args:
        start ([tuple]): Starting point
        end ([tuple]): Ending point

    Returns:
        [tuple]: (k,m) where y = k*x + m
    """    
    if start[0] == end[0]:
        if start[0] > end[0]:
            # y = 0*x + m
            return [0, start[0]]
        else :
            # y = 0*x - m
            return [0, -1*start[0]]
    elif start[1] == end[1]:
        if start[1] > end[1]:
            # y = k*x
            return [start[1], 0]
        else :
            # y = -k*x
            return [-1*start[1], 0]
    else:
        xCord = [start[0], end[0]]
        yCord = [start[1], end[1]]
        newTraj = np.polyfit(xCord,yCord,1)
        # y = k*x + m
        return newTraj

# Collision
def collision(x1,x2):
    """Check if two objects are on path to collide

    Args:
        x1 ([tuple]): Curent position if first object
        x2 ([tuple]): Curent position if second object

    Returns:
        [bool]: True if they could collide, False if they won't
    """    
    # Distance between two objects (Pythagorean theorem)
    dist = sqrt(abs((x1[0] - x2[0])**2 + (x1[1] - x2[1]**2)))
    if dist > safeDistance:
        return False
    else:
        return True

def endingZone(x1,x2):
    """Check if object is close enough to the end

    Args:
        x1 ([tuple]): Current position of object
        x2 ([tuple]): Ending or goal position

    Returns:
        [bool]: True if it's close, False if it's not
    """    
    # (Pythagorean theorem)
    dist = sqrt(abs((x1[0] - x2[0])**2 + (x1[1] - x2[1])**2))
    if dist > 1:
        return False
    else:
        return True

# Find angle
def findAngle(x1, x2):
    """ Finds angle between trajectory and coordinate system

    Args:
        x1 ([tuple]): Starting point
        x2 ([tuple]): Ending point

    Returns:
        [int]: Angle in radians
    """    
    x = x2[0] - x1[0]
    y = x2[1] - x1[1]
    return atan(y/x)

# Find speed vector components
def findSpeedComponents(point,endPoint,linEq):
    """ Calculate x and y components of speed vector

    Args:
        point ([tuple]): Current point
        endPoint ([tuple]): Ending point
        linEq ([tuple]): Current trajectory

    Returns:
        [tuple]: x and y components of speed vector
    """    
    if linEq[0] > 0 and linEq[1] != 0:
        angle = findAngle(point, endPoint)
        speedComponentX = cos(angle) * Vmax
        speedComponentY  = sin(angle) * Vmax
        return [speedComponentX, speedComponentY]
    elif linEq[0] < 0 and linEq[1] != 0:
        angle = findAngle(point, endPoint)
        speedComponentX = cos(angle) * Vmax
        speedComponentY  = sin(angle) * Vmax
        return [-1*speedComponentX, -1*speedComponentY]
    elif linEq[1] == 0:
        if linEq[0] > 0:
            return [-1*Vmax, 0]
        else:
            return [Vmax, 0]
    elif linEq[0] == 0:
        if linEq[1] > 0:
            return [0, -1*Vmax]
        else:
            return [0, Vmax]
    else:
        return ValueError

# %% Main

# Calculate starting trajectories
for i in range(len(currentEq)):
    currentEq[i] = trajectory(startingPoint[i],endingPoint[i])

# Check if we can start from starting positions
for i in range(1,len(indexes)):
    res = collision(currentState[i-1], currentState[i])
    if res:
        hold[i] = True

for i in indexes:
    currentSpeed[i] = findSpeedComponents(currentState[i], endingPoint[i], currentEq[i])

# sin^2 + cos^2 = 1
# for i in range(len(currentSpeed)):
#     print(currentSpeed[i][0]**2 + currentSpeed[i][1]**2)

# Have we reached end point
end = [False, False, False]


while True:
    # Iterate through the indexes of object 
    for i in indexes:
        if end[i] == False:
            point = currentState[i]
            for j in indexes:
                # Check for the collision
                if collision(currentState[j], currentState[i]):
                    if j>i:
                        getReadyToEvade[i] = True
                    elif j<i:
                        hold[i] = True
                    else: continue
            # Action if object needs to hold
            if hold[i]:
                currentState[i] = (currentState[i][0]+Vmax/2, currentState[i][1]-Vmax/2)
                history[i].append(currentState[i])
                currentEq[i] = trajectory(currentState[i],endingPoint[i])
                currentSpeed[i] = findSpeedComponents(currentState[i], endingPoint[i], currentEq[i])
                hold[i] = False
            # Action if object needs to evade
            elif getReadyToEvade[i]:
                currentState[i] = (currentState[i][0]-Vmax/2, currentState[i][1]+Vmax/2)
                history[i].append(currentState[i])
                currentEq[i] = trajectory(currentState[i],endingPoint[i])
                currentSpeed[i] = findSpeedComponents(currentState[i], endingPoint[i], currentEq[i])
                getReadyToEvade[i] = False
            # Action if object can move to next point undisturbed
            else:  
                # From top to bottom
                if startingPoint[i][1] > endingPoint[i][1]:
                    newPointX = point[0] - currentSpeed[i][0]
                    newPointY = point[1] - currentSpeed[i][1] 
                    currentState[i] = (newPointX, newPointY)
                    history[i].append(currentState[i])
                # From bottom to top
                else:                    
                    newPointX = point[0] + currentSpeed[i][0]
                    newPointY = point[1] + currentSpeed[i][1] 
                    currentState[i] = (newPointX, newPointY)
                    history[i].append(currentState[i])
            # Check if object reached ending zone
            if endingZone(endingPoint[i], currentState[i]):
                end[i] = True
            else: pass

    if False in end:
        continue
    # If all object reached ending zone finish
    else: break

# History for each object
X1 = history[0]
X2 = history[1]
X3 = history[2]
# print(X1)
# print("----------")
# print(X2)
# print("----------")
# print(X3)
# print("----------")

xVal = [x[0] for x in X1]
yVal = [x[1] for x in X1]
plt.plot(xVal, yVal, 'ro', label="X1")

xVal = [x[0] for x in X2]
yVal = [x[1] for x in X2]
plt.plot(xVal, yVal, 'bo', label="X2")

xVal = [x[0] for x in X3]
yVal = [x[1] for x in X3]
plt.plot(xVal, yVal, 'go', label="X3")

plt.legend()
plt.grid()
# %%
