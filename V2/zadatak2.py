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
#   1 - we can go from one node to the other
#  -1 - we can not go from one node to the other
#
#     A B C D E
#   A[ 0 -1  1  0  0]
#   B[ 1  0  0 -1  1]
#   C[-1  0  0  1  0]
#   D[ 0  1 -1  0  1]
#   E[ 0 -1  0 -1  0]

A = [[0, -1, 1, 0, 0], [1, 0, 0, -1, 1], [-1, 0, 0, 1, 0], [0, 1, -1, 0, 1], [0, -1, 0, -1, 0]]

v = [-np.inf for i in range(len(A))]
v[-1] = 0
# %% Checking if A matrix is symetric
# If matrix A is symetric then we can move in both directions
# if matrix A is not symetric than we can move in only one direction

def transpose(mat, tr, N): 
    for i in range(N): 
        for j in range(N): 
            tr[i][j] = mat[j][i]

def isSymmetric(mat, N):      
    tr = [ [0 for j in range(len(mat[0])) ] for i in range(len(mat)) ] 
    transpose(mat, tr, N) 
    for i in range(N): 
        for j in range(N): 
            if (mat[i][j] != tr[i][j]): 
                return False
    return True

if (isSymmetric(A, 5)):
    factor = 1
    print('Matrix A is symetric')
else:
    factor = -1
    print('Matrix A is not symetric')

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
        if x == factor:
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
