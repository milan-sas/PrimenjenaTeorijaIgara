# %% Define

import numpy as np
import matplotlib.pyplot as plt

# %% Check input

def checkInput():
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
            raise ValueError("Invalid node!!! Please choose valid node im ragne (A-E)")
    except Exception as identifier:
        print(identifier)
        return checkInput()
# %% Find shortest path

def shortestPath(startNode, endNode, val):
    """Find shortest path from starting node to terminal node

    Args:
        startNode ([int]): Index of starting node
        endNode ([int]): Index of terminal node
        val ([list]): Values for each node counting from the terminal node

    Returns:
        [list]: Shortest path from starting to terminal node
    """    
    current = val[startNode]
    path = [startNode]
    while current != 0:
        for (j,temp) in enumerate(val):
            if current == temp-1:
                current = temp
                path.append(j)
                break
            else:
                continue
    return path

def printPath(p):
    """Creates list of letter symbols insted of numbers

    Args:
        p ([list]): List of nodes as numbers

    Returns:
        [list]: List of nodes as letters
    """    
    output = []
    for k in p:
        if k == 0:
            output.append('A')
        elif k == 1:
            output.append('B')
        elif k == 2:
            output.append('C')
        elif k == 3:
            output.append('D')
        elif k == 4:
            output.append('E')
        elif k == 5:
            output.append('F')
        else:
            output.append('Unknown index')
    return output

# %% Creating graph and getting input

# Its adjacency matrix (matrica susedstva):
#     A B C D E
#   A[0 1 1 0 0]
#   B[1 0 0 1 1]
#   C[1 0 0 1 0]
#   D[0 1 1 0 1]
#   E[0 1 0 1 0]

A = [[0, 1, 1, 0, 0], [1, 0, 0, 1, 1], [1, 0, 0, 1, 0], [0, 1, 1, 0, 1], [0, 1, 0, 1, 0]]

v = [-np.inf for i in range(len(A))]

print("Please enter a terminal node (A-E)")
terminalNode = checkInput()

print("Please enter a starting node (A-E)")
startingNode = checkInput()

while terminalNode == startingNode:
    print("Invalid starting node! Starting and terminal node can not be the same")
    startingNode = checkInput()

v[terminalNode] = 0
# %% Getting values for every node starting from terminal one

# Stert from terminal node
nodesToCheck = [terminalNode]

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

shPath = shortestPath(startingNode, terminalNode, v)
print(shPath)

prettyPrint = printPath(shPath)
print('Shortest path:')
print(prettyPrint)
# %%
