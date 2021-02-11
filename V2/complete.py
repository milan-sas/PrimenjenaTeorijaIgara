# %% Define

import numpy as np
import matplotlib.pyplot as plt

# %% Graph setting up
'''
The following examples are used for testing in development of this code.
If you want to use one of A examples just remove #
'''

'''
Its adjacency matrix for task 1:
    A B C D E
  A[0 1 1 0 0]
  B[1 0 0 1 1]
  C[1 0 0 1 0]
  D[0 1 1 0 1]
  E[0 1 0 1 0]
'''
A = [[0, 1, 1, 0, 0], [1, 0, 0, 1, 1], [1, 0, 0, 1, 0], [0, 1, 1, 0, 1], [0, 1, 0, 1, 0]]

'''
Its adjacency matrix for task 2:
 |1| represents connection between two nodes
  1 - we can go from one node to the other
 -1 - we can not go from one node to the other

     A  B  C  D  E
  A[ 0 -1  1  0  0]
  B[ 1  0  0 -1  1]
  C[-1  0  0  1  0]
  D[ 0  1 -1  0  1]
  E[ 0 -1  0 -1  0]
  '''
#A = [[0, -1, 1, 0, 0], [1, 0, 0, -1, 1], [-1, 0, 0, 1, 0], [0, 1, -1, 0, 1], [0, -1, 0, -1, 0]]

'''
Adjacency matrix fot task 4:
    A B C D E
  A[0 2 3 0 0]
  B[2 0 0 3 2]
  C[3 0 0 1 0]
  D[0 3 1 0 1]
  E[0 2 0 1 0]
'''
#A = [[0, 2, 3, 0, 0], [2, 0, 0, 3, 2], [3, 0, 0, 1, 0], [0, 3, 1, 0, 1], [0, 2, 0, 1, 0]]
'''
Adjacency matrix fot tasks 2 and 4:
     A  B  C  D  E
  A[ 0 -2  3  0  0]
  B[ 2  0  0 -3  2]
  C[-3  0  0  1  0]
  D[ 0  3 -1  0  1]
  E[ 0 -2  0 -1  0]
'''
#A = [[0, -2, 3, 0, 0], [2, 0, 0, -3, 2], [-3, 0, 0, 1, 0], [0, 3, -1, 0, 1], [0, -2, 0, -1, 0]]

# %% Checking if A matrix is symetric
# If matrix A is symetric then we can move in both directions
# if matrix A is not symetric than we can move in only one direction

def transpose(mat, tr, N):
    """Transpose matrix 

    Args:
        mat (list): Original NxN matrix
        tr (list): Empty NxN matrix 
        N (int): Size of original matrix of graph
    """     
    for i in range(N): 
        for j in range(N): 
            tr[i][j] = mat[j][i]

def isSymmetric(mat, N):      
    """Checking if matrix mat is symetric
        - If matrix is symetric then we have an undirected graph
        - if matrix is not symetric thwn we have a directed graph

    Args:
        mat (list): Original NxN matrix
        N (int): Size of original matrix of graph

    Returns:
        [bool]: Is original matrix symetric or not
    """    
    tr = [ [0 for j in range(len(mat[0])) ] for i in range(len(mat)) ] 
    transpose(mat, tr, N) 
    for i in range(N): 
        for j in range(N): 
            if (mat[i][j] != tr[i][j]): 
                return False
    return True

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

def checkTerminalNodesNumber():
    """ Checking if index of node is valid

    Raises:
        ValueError: Invalid input!!! Please choose valid terminal nodes in ragne (1-4)

    Returns:
        [int]: Index of selected node
    """    
    try:
        a = int(input())
        if 0 < a <=4:
            return a
        else:
            raise ValueError("Invalid input!!! Please choose valid terminal nodes in ragne (1-4)")
    except Exception as identifier:
        print(identifier)
        return checkTerminalNodesNumber()

# %% Find shortest path

def shortestPath(startNode, val, M):
    """Find shortest path from starting node to terminal node

    Args:
        startNode (int): Index of starting node
        val (list): Values for each node counting from the terminal node(s)
        M (list): Original matrix of graph

    Returns:
        [list]: Shortest path from starting to terminal node
    """
    current = val[startNode]
    index = startNode
    path = [startNode]
    while current != 0:
        for (j,temp) in enumerate(val):
            if (current == temp - M[index][j]) and (M[index][j] > 0):
                current = temp
                index = j
                path.append(j)
                break
            else:
                continue
    return path

def printPath(p):
    """Creates list of letter symbols insted of numbers

    Args:
        p (list): List of nodes as numbers

    Returns:
        [int]: Returns only one node as letter
            or
        [list]: List of nodes as letters
    """    
    # Checking if p is only one number (type = int)
    if isinstance(p, int):
        if p == 0:
            return("A")
        elif p== 1:
            return("B")
        elif p == 2:
            return("C")
        elif p == 3:
            return("D")
        elif p == 4:
            return("E")
        elif p == 5:
            return("F")
        else:
            return('Unknown index')
    # If p is a list then we do the following instructions
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


# %% Main

print("Please enter number of terminal nodes (1-4)")
terminalNumber = checkTerminalNodesNumber()
terminalList = []

print("Please enter a terminal node (A-E)")

while (terminalNumber != 0):
    terminalList.append(checkInput())
    terminalNumber = terminalNumber - 1

print("Please enter a starting node (A-E)")
startingNode = checkInput()

while (startingNode in terminalList):
    print("Invalid starting node! Starting and terminal node can not be the same")
    startingNode = checkInput()

print("Terminal node(s):")
print(printPath(terminalList))

print("Starting node")
print(printPath(startingNode))


v = [-np.inf for i in range(len(A))]


if (isSymmetric(A, 5)):
    factor = 1
    print('Matrix A is symetric')
else:
    factor = 0
    print('Matrix A is not symetric')


if factor == 1:
    # For every terminal node we will check nodes values
    for currentTerminal in terminalList:
        v[currentTerminal] = 0
        nodesToCheck = [currentTerminal]
        while True:
            if len(nodesToCheck) == 0:
                print("Done for the current terminal node")
                break
            currentNode = nodesToCheck.pop()
            neighbours = []
            # Fidns index of all neighbours of current node
            for (i,x) in enumerate(A[currentNode]):
                if x > 0:
                    neighbours.append(i)

            for n in neighbours:
                # A[n][currentNode] is value of edge between two nodes
                newValue = v[currentNode] - A[n][currentNode]
                if v[n] >= newValue:
                    continue
                else:
                    v[n] = newValue
                    nodesToCheck.append(n)
else:
    # For every terminal node we will check nodes values
    for currentTerminal in terminalList:
        v[currentTerminal] = 0
        nodesToCheck = [currentTerminal]
        while True:
            if len(nodesToCheck) == 0:
                print("Done for the current terminal node")
                break
            currentNode = nodesToCheck.pop()
            neighbours = []
            # Fidns index of all neighbours of current node
            for (i,x) in enumerate(A[currentNode]):
                if x < 0:
                    neighbours.append(i)

            for n in neighbours:
                # A[n][currentNode] is value of edge between two nodes
                newValue = v[currentNode] + A[currentNode][n]
                if v[n] >= newValue:
                    continue
                else:
                    v[n] = newValue
                    nodesToCheck.append(n)

# Prints values of every node in graph
print(v)
# Shortest path from startin to ending node
shPath = shortestPath(startingNode, v, A)
# Same thing but with letters instead of numbers
prettyPrint = printPath(shPath)
print('Shortest path:')
print(prettyPrint)
# %%
