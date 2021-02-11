# %% Define

import numpy as np
import matplotlib.pyplot as plt

# %% Setting up

# Graph:
# A B C D F
#     
# B A A B B
# C D D C D
#   E   E

# Its adjacency matrix (matrica susedstva):
#     A B C D E
#   A[0 1 1 0 0]
#   B[1 0 0 1 1]
#   C[1 0 0 1 0]
#   D[0 1 1 0 1]
#   E[0 1 0 1 0]

A = [[0, 1, 1, 0, 0], [1, 0, 0, 1, 1], [1, 0, 0, 1, 0], [0, 1, 1, 0, 1], [0, 1, 0, 1, 0]]


# Nodes A and E are terminal ones
#v[-1] = 0
# %% Input for terminal nodes 

def checkNodeInput():
    """Checking in input is in valid range (A-E)

    Raises:
        ValueError: Input is not in valid range

    Returns:
        [int]: Index of the node in the graph
    """    
    try:
        a = input()
        if a == 'A' or a == 'a':
            return 0
        elif a == 'B' or a == 'b':
            return 1
        elif a == 'C' or a == 'c':
            return 2
        elif a == 'D' or a == 'd':
            return 3
        elif a == 'E' or a == 'e':
            return 4
        elif a == 'F' or a == 'f':
            return 5
        else:
            raise ValueError("Invalid node!!! Please choose valid node in ragne (A-B)")
    except Exception as identifier:
        print(identifier)
        return checkNodeInput()

def checkTerminalNodesNumber():
    try:
        a = int(input())
        if 0 < a <=4:
            return a
        else:
            raise ValueError("Invalid input!!! Please choose valid terminal nodes in ragne (1-4)")
    except Exception as identifier:
        print(identifier)
        return checkTerminalNodesNumber()

# %% Main

v = [-np.inf for i in range(len(A))]

print("Please enter number of terminal nodes")
terminalNumber = checkTerminalNodesNumber()
terminalList = []

print("Please enter terminal node")
while (terminalNumber != 0):
    terminalList.append(checkNodeInput())
    terminalNumber = terminalNumber - 1
print("Terminal nodes:")
print(terminalList)

for currentTerminal in terminalList:
    v[currentTerminal] = 0
    nodesToCheck = [currentTerminal]
    while True:
        if len(nodesToCheck) == 0:
            print("Done")
            break
        currentNode = nodesToCheck.pop()
        neighbours = []
        # Fidns index of all neighbours of current node
        for (i,x) in enumerate(A[currentNode]):
            if x == 1:
                neighbours.append(i)

        for n in neighbours:
            newValue = v[currentNode] - 1
            if v[n] >= newValue:
                continue
            else:
                v[n] = newValue
                nodesToCheck.append(n)

print(v)

# %%

# %%
