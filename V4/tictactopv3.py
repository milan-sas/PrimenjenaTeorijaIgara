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
        return boardState[3]

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
    if state != playerNone:
        return True
    for player in boardState:
        if player == playerNone:
            return False
    return True

# %% Reward

def reward(player, boardState):
    if player == playerX:
        return lose
    elif player == playerO:
        return win
    else:
        if freeSpace(boardState) == []:
            return draw
        else: return None

# %% Q Laerning

def bestMove(boardState):
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
        else:
            nexBoardState[pos] = playerNone

    s =  {k: v for k, v in sorted(s.items(), key=lambda item: item[1])}

    for ret in s:
        if s[ret] == 1:
            return ret
        elif s[ret] == 0.5:
            return ret
        else:
            returnList.append(ret)
    
    return returnList[np.random.randint(0,len(returnList))]
    
      
# !!!!!!!!! OVO JE UPITNO !!!!!!!!!
Q = []

def qlearning(s, Q, boardState, rew, a=0, aplha=0.1, gamma=0.9):

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
    possibleMoves = freeSpace(boardState)
    return possibleMoves[np.random.randint(0,len(possibleMoves))]

# %% Policy

def epsGreedy(boardState, Q, eps = 0.1):
    possible = []
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
    boardState = [playerNone,playerNone,playerNone,
                  playerNone,playerNone,playerNone,
                  playerNone,playerNone,playerNone,]
    res = None
    state = None

    while True:
        x = opponent(boardState)
        boardState[x] = playerX

        # print('-------------------------')
        # print((boardState[0], boardState[1], boardState[2]))
        # print((boardState[3], boardState[4], boardState[5]))
        # print((boardState[6], boardState[7], boardState[8]))

        rew = winner(boardState)
        if rew == playerX:
            rew = lose
            break
        elif playerNone not in boardState:
            rew = draw
            break
        else:
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
for i in range(20000):
    Q, r, board= playOneGame(Q)
    # print((board[0], board[1], board[2]))
    # print((board[3], board[4], board[5]))
    # print((board[6], board[7], board[8]))
    resultList.append(r)
    # print(sum(resultList)/len(resultList))
    print('Game : ' + str(i))

    

print('-------------------------')
print(sum(resultList)/len(resultList))
















# %%
