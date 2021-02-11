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

# %% Reward

def reward(player, boardState):
    """ Check reward for current board state

    Args:
        player ([int]): Player who made the lastets move
        boardState ([type]): Current state on board

    Returns:
        [int]: lose if X won the game, win if O won the game, draw if it's a draw or None if it's not the end of a game
    """    
    if player == playerX:
        return lose
    elif player == playerO:
        return win
    elif len(freeSpace(boardState)) == 0:
        return draw
    else: return None

# %% Q Laerning

def bestMoveO(boardState):
    """Find best move for current state and player O
        Each move has value:
            1 if it's gonna bring wictory for player O
            0.5 if it's gonna bring loss for player O
            0 if it won't finish the  game

    Args:
        boardState ([list]): Current state on board

    Returns:
        [int]: Best move for current state and player O
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
        # Set to default state
        nexBoardState[pos] = playerNone

    s =  {k: v for k, v in sorted(s.items(), key=lambda item: item[1], reverse=True)}

    for ret in s:
        # If we can win we should play this move
        if s[ret] == 1:
            return ret
        # if we can lose we should play this move
        elif s[ret] == 0.5:
            return ret
        else:
            returnList.append(ret)
    
    return returnList[np.random.randint(0,len(returnList))]
    
def bestMoveX(boardState, lastMove):
    """Find best move for current state and player X

    Args:
        boardState ([list]): Current state on board
        lastMove ([int]): If game is a draw then X played the last move

    Returns:
        [int]: Best move for current state and player X
    """    
    s = {}
    returnList = []
    nexBoardState = boardState[:]
    free = freeSpace(boardState)

    if len(freeSpace(boardState)) == 0:
        return lastMove
    
    for pos in free:
        s[pos] = draw

    for pos in s:
        nexBoardState[pos] = playerO
        # Will the next move bring me loss?
        if winner(nexBoardState) == playerO:
            s[pos] = 0.5
        # Will the next move bring me victory?
        nexBoardState[pos] = playerX
        if winner(nexBoardState) == playerX:
            s[pos] = 1        
        
        nexBoardState[pos] = playerNone

    s =  {k: v for k, v in sorted(s.items(), key=lambda item: item[1], reverse=True)}

    for ret in s:
        # If we can win we should play this move
        if s[ret] == 1:
            return ret
        # If we can lose we should play this move
        elif s[ret] == 0.5:
            return ret
        else:
            returnList.append(ret)
    
    return returnList[np.random.randint(0,len(returnList))]
      

Qx = []
Qo = []

def qlearning(cnt, s, Q, boardState, rew, aplha=0.1, gamma=0.9):
    """QLearning method for updateing Q table

    Args:
        cnt ([int]): 1 if it's X turn, 2 if it's O turn
        s ([int]): Move played by current player
        Q ([list]): Q table for current player
        boardState ([list]): Current state on board
        rew ([float]): Reward for move
        aplha (float, optional): Defaults to 0.1.
        gamma (float, optional): Defaults to 0.9.

    Returns:
        [list]: Updated Q table for current player
    """    

    # Fand best move for O player
    if cnt == 2:
        best = bestMoveO(boardState)
    # Find best move for X player
    else:
        best = bestMoveX(boardState, s)
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

# %% Policy

def epsGreedy(cnt, boardState, Q, eps = 0.01):
    """Eps greedy policy

    Args:
        cnt ([int]): 1 if it's X turn, 2 if it's O turn
        boardState ([list]): Current state on board
        Q ([list]): Q table for current player
        eps (float, optional): Defaults to 0.01.

    Returns:
        [int]: Move for current player
    """    
    possible = []
    if np.random.rand() < eps:
        # Random move
        f = freeSpace(boardState)
        return f[np.random.randint(0,len(f))]
    else:
        # Greedy move
        if cnt == 2:
            best = bestMoveO(boardState)
        else:
            best = bestMoveX(boardState, None)
        return best

# %% Play one game

# Opponent X always plays first
def playOneGame(Qx, Qo):
    """ Simulates one game of tic-tac-toe

    Args:
        Qx ([list]): Q table for X player
        Qo ([list]): Q table for O player

    Returns:
        [touple]: New Qx, new Qo, result and board state
    """    
    boardState = [playerNone,playerNone,playerNone,
                  playerNone,playerNone,playerNone,
                  playerNone,playerNone,playerNone,]
    rew = None
    state = None

    while True:
        x = epsGreedy(1, boardState, Qx)
        boardState[x] = playerX

        # print('-------------------------')
        # print((boardState[0], boardState[1], boardState[2]))
        # print((boardState[3], boardState[4], boardState[5]))
        # print((boardState[6], boardState[7], boardState[8]))

        rew = reward(winner(boardState), boardState)
        if rew == None:
            Qx = qlearning(1, x, Qx, boardState,rew=0.5)
        else:
            if rew == lose:
                # Update Q
                Qx = qlearning(1, x, Qx, boardState,rew)
                break
            elif rew == draw:
                Qx = qlearning(1, x, Qx, boardState,rew)
                break
        
        o = epsGreedy(2, boardState, Qo)
        boardState[o] = playerO

        # print('-------------------------')
        # print((boardState[0], boardState[1], boardState[2]))
        # print((boardState[3], boardState[4], boardState[5]))
        # print((boardState[6], boardState[7], boardState[8]))

        rew = reward(winner(boardState), boardState)
        if rew == win:
            # Update Q
            Qo = qlearning(2, o, Qo, boardState,rew)
            break
        elif rew == lose:
            Qo = qlearning(2, o, Qo, boardState,rew)
            break
        elif rew == draw:
            Qo = qlearning(2, o, Qo, boardState,rew)
            break
        else:
            Qo = qlearning(2, o, Qo, boardState,rew=0.5)
        

    return Qx, Qo, rew, boardState

# %% Main
board = []
resultListX = []
resultListO = []

for i in range(10000):
    Qx, Qo, r, board= playOneGame(Qx, Qo)
    # print('-------------------------')
    # print((board[0], board[1], board[2]))
    # print((board[3], board[4], board[5]))
    # print((board[6], board[7], board[8]))
    resultListO.append(r)
    resultListX.append(-1*r)
    print('Game : ' + str(i))    

print('-------------------------')
print('Result for X: ' + str(sum(resultListX)/len(resultListX)))
print('Result for O: ' + str(sum(resultListO)/len(resultListO)))

# %%
