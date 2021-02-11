# %% Define

import numpy as np
import matplotlib.pyplot as plt

# %%

# Graph:
# A B C D F
#     
# B A A B B
# C D D C D
#   E   E

# Its adjacency matrix (matrica susedstva):
#     A B C D E
#   A[0 2 3 0 0]
#   B[2 0 0 3 2]
#   C[3 0 0 1 0]
#   D[0 3 1 0 1]
#   E[0 2 0 1 0]

A = [[0, 2, 3, 0, 0], [2, 0, 0, 3, 2], [3, 0, 0, 1, 0], [0, 3, 1, 0, 1], [0, 2, 0, 1, 0]]

v = [-np.inf for i in range(len(A))]
v[-1] = 0
# %% Main

# Laste node is the terminal one
nodesToCheck = [len(A)-1]

while True:
    if len(nodesToCheck) == 0:
        print("Done")
        break
    currentNode = nodesToCheck.pop()
    neighbours = []
    # Fidns index of all neighbours of current node
    for (i,x) in enumerate(A[currentNode]):
        if x >= 1:
            neighbours.append(i)

    for n in neighbours:
        newValue = v[currentNode] - A[n][currentNode]
        if v[n] >= newValue:
            continue
        else:
            v[n] = newValue
            nodesToCheck.append(n)

print(v)

# %%
