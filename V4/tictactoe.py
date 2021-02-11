# %% Define Tic tac toe board
import numpy as np
import random

playerNone = 0
playerO = 1
playerX = 2

win = 1
draw = 0
lose = -1

boardState = [playerNone,playerNone,playerNone,
              playerNone,playerNone,playerNone,
              playerNone,playerNone,playerNone,]

def winner(boardState):
    """ Check if we have a winner in current state

    Args:
        boardState ([list]): Current state on board

    Returns:
        [int]: 1 if O won, 2 if X won, 0 we dont have a winner yet
    """    
    # Horizontal lines
    if boardState[0] != playerNone and boardState[0] == boardState[1] and boardState[0] == boardState[2]:
        return boardState[0]
    if boardState[3] != playerNone and boardState[3] == boardState[4] and boardState[3] == boardState[5]:
        return boardState[3]
    if boardState[6] != playerNone and boardState[6] == boardState[7] and boardState[6] == boardState[8]:
        return boardState[6]

    # Vertical lines
    if boardState[0] != playerNone and boardState[0] == boardState[3] and boardState[0] == boardState[6]:
        return boardState[0]
    if boardState[1] != playerNone and boardState[1] == boardState[4] and boardState[1] == boardState[7]:
        return boardState[1]
    if boardState[2] != playerNone and boardState[2] == boardState[5] and boardState[2] == boardState[8]:
        return boardState[2]

    # Diagonal lines
    if boardState[0] != playerNone and boardState[0] == boardState[4] and boardState[0] == boardState[8]:
        return boardState[0]
    if boardState[6] != playerNone and boardState[6] == boardState[4] and boardState[6] == boardState[2]:
        return boardState[6]

    return playerNone

def freeSpace(boardState):
    """Check avilable positions on borad

    Args:
        boardState ([list]): Current state on board

    Returns:
        [list]: List of avilable positions on board
    """    
    res = []
    for pos, player in enumerate(boardState):
        if player == playerNone:
            res.append(pos)
    return res

def terminalState(state, boardState):
    """Check if we are in termianl state

    Args:
        state ([int]): Result of winner() function
        boardState ([list]): Current state on board

    Returns:
        [bool]: True if it's end of a game, False if it's not
    """    
    if winner(boardState) != playerNone:
        return True
    for player in boardState:
        if player == playerNone:
            return False
    return True

# %% Reward

def reward(player, boardState):
    """Returns result of one game

    Args:
        player ([int]): playerX or playerO
        boardState ([list]): Current state on board

    Returns:
        [int]: Result of game
    """    
    if player == playerX:
        return lose
    elif player == playerO:
        return win
    elif len(freeSpace(boardState)) == 0:
        return draw
    else: return None

# %% Q Laerning

def bestMove(boardState):
    """ Returns best move by Greedy policy

    Args:
        boardState ([list]): Current state on board

    Returns:
        [int]: Position of best move
    """    
    s = {}
    returnList = []
    nexBoardState = boardState[:]
    free = freeSpace(boardState)
    
    for pos in free:
        s[pos] = draw

    for pos in s:
        nexBoardState[pos] = playerX
        # Will the next move bring me loss?
        if winner(nexBoardState) == playerX:
            s[pos] = 0.5
        # Will the next move bring me victory?
        nexBoardState[pos] = playerO
        if winner(nexBoardState) == playerO:
            s[pos] = 1    

        nexBoardState[pos] = playerNone

    s =  {k: v for k, v in sorted(s.items(), key=lambda item: item[1], reverse=True)}

    for ret in s:
        if s[ret] == 1:
            return ret
        elif s[ret] == 0.5:
            return ret
        else:
            returnList.append(ret)
    
    return returnList[np.random.randint(0,len(returnList))]
    
Q = []

def qlearning(s, Q, boardState, rew, a=0, aplha=0.1, gamma=0.9):
    """ Q learning 

    Args:
        s ([int]): Position on board
        Q ([type]): Q table
        boardState ([list]): Current state on board
        rew ([float]): Reward for current state
        a (int, optional): Defaults to 0.
        aplha (float, optional):  Defaults to 0.1.
        gamma (float, optional):  Defaults to 0.9.

    Returns:
        [list]: New Q table
    """    

    best = bestMove(boardState)
    newState = True

    for q in Q:
        if q[0] == boardState:
            q[1] = q[1] + aplha*(rew + gamma*best - q[1])
            newState = False
        else:
            pass
    if newState:
        Q.append([boardState, 0.5])
    return Q

# %% Opponent

def opponent(boardState):
    """Opponent or X player who plays random moves

    Args:
        boardState ([list]): Current state on board

    Returns:
        [int]: Move for X player
    """    
    possibleMoves = freeSpace(boardState)
    return possibleMoves[np.random.randint(0,len(possibleMoves))]

# %% Policy

def epsGreedy(boardState, Q, eps = 0.01):
    """Eps greedy policy

    Args:
        boardState ([list]): Current state on board
        Q ([list]): Q table
        eps (float, optional): . Defaults to 0.1.

    Returns:
        [int]: Move for O player based on policy
    """    
    f = []
    if np.random.rand() < eps:
        # Random move
        f = freeSpace(boardState)
        return f[np.random.randint(0,len(f))]
    else:
        # Greedy move
        best = bestMove(boardState)
        return best

# %% Play one game

# Opponent X always plays first
def playOneGame(Q):
    """ Simulates one game of tic tac top

    Args:
        Q ([lsit]): Q table

    Returns:
        [list]: New Q table
    """    
    boardState = [playerNone,playerNone,playerNone,
                  playerNone,playerNone,playerNone,
                  playerNone,playerNone,playerNone,]
    rew = None

    while True:
        x = opponent(boardState)
        boardState[x] = playerX

        # print('-------------------------')
        # print((boardState[0], boardState[1], boardState[2]))
        # print((boardState[3], boardState[4], boardState[5]))
        # print((boardState[6], boardState[7], boardState[8]))

        rew = reward(winner(boardState), boardState)
        if rew == lose:
            break
        elif rew == draw:
            break
        
        o = epsGreedy(boardState, Q)
        boardState[o] = playerO

        # print('-------------------------')
        # print((boardState[0], boardState[1], boardState[2]))
        # print((boardState[3], boardState[4], boardState[5]))
        # print((boardState[6], boardState[7], boardState[8]))
        
        rew = reward(winner(boardState), boardState)
        if rew == win:
            # Update Q
            Q = qlearning(o, Q, boardState,rew)
            break
        elif rew == lose:
            Q = qlearning(o, Q, boardState,rew)
            break
        elif rew == draw:
            Q = qlearning(o, Q, boardState,rew)
            break
        else:
            Q = qlearning(o, Q, boardState,rew=0.5)
            continue
        

    return Q, rew, boardState

# %% Main
board = []
resultList = []
for i in range(10000):
    Q, r, board= playOneGame(Q)
    # print((board[0], board[1], board[2]))
    # print((board[3], board[4], board[5]))
    # print((board[6], board[7], board[8]))
    resultList.append(r)
    # print(sum(resultList)/len(resultList))
    print('Game: ' + str(i))

for res in resultList:
    if res == 0:
        resultList.remove(res)    

print('-------------------------')
print(sum(resultList)/len(resultList))
print('Lets play some tic-tac-toe')
# %%
