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
#   A[0 1 1 0 0]
#   B[1 0 0 1 1]
#   C[1 0 0 1 0]
#   D[0 1 1 0 0]
#   E[0 1 0 1 0]

A = [[0, 1, 1, 0, 0], [1, 0, 0, 1, 1], [1, 0, 0, 1, 0], [0, 1, 1, 0, 0], [0, 1, 0, 1, 0]]

v = [-np.inf for i in range(len(A))]
v[-1] = 0
# %%

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
        if x == 1:
            neighbours.append(i)

    for n in neighbours:
        newValue = v[currentNode] - 1
        if v[n] >= newValue:
            continue
        else:
            v[n] = newValue
            nodesToCheck.append(n)

# %%
