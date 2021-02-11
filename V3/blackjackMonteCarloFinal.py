# %% Define

import numpy as np
from numpy.random import rand, randint


# %%  Draw card function

# One full deck of cards
deck =  [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

def drawCard():
    """Functions returns one card from deck

    Returns:
        [int]: Value of card drawn from the deck
    """    
    # Range if index: 0-51
    card = round(rand()*51)
    return deck[card]

# %% Decision policy

def epsGreedy(Q, state, eps = 0.01):
    """ EPS Greedy decision policy

    Args:
        Q (list): Table of all states and played actions
        state (tuple): Current sum of players cards, info about usable ace, dealer card
        eps (float, optional): EPS parameter. Defaults to 0.1.

    Returns:
        [tuple]: 0 if action is HIT, 1 if ation is hold and sum uset to calculate moves
    """    
    hitMoves = []
    holdMoves = []
    currentSum, ace, dealer = state
    if dealer == 1:
        dealer = 11
    if ace and currentSum <= 11:
        currentSum += 10
    if currentSum == 21:
        return 1, currentSum
    if currentSum < 17:
        return 0, currentSum
    if rand() < eps:
        # Random hit or hold 
        tmp = rand()
        if tmp >= 0.5:
            # HIT
            return 0, currentSum
        else:
            # HOLD
            return 1, currentSum
    else:
        # Greedy policy 
        if currentSum <= 11 and dealer <= 7:     
            return 0, currentSum
        elif 17 - dealer >= 21 - currentSum:
            return 1, currentSum
        elif dealer + 10 > currentSum and dealer < 7:
            return 0, currentSum
        # elif dealer + 10 < currentSum:
        #     return 1, currentSum
        else: pass
        arr = np.array(Q)
        res = np.where(arr == currentSum)
        try:
            hitMoves = Q[res[0][0]][1]
            holdMoves = Q[res[0][0]][2]
            if sum(hitMoves) > sum(holdMoves):
                return 0, currentSum
            elif sum(hitMoves) > sum(holdMoves):
                return 1, currentSum
            elif len(hitMoves) > len(holdMoves):
                return 1, currentSum
            else:
                return 0, currentSum
        except:
            # Try moves that you didn't play before
            if hitMoves == []:
                return 0, currentSum
            elif holdMoves == []:
                return 1, currentSum
            else:
                return 0, currentSum

# %% Play One Real Game

def playGame(Q):
    """Simulates one game of Blackjack

    Returns:
        [int]: 1 if player wins, -1 if dealer wins, 0 if it's draw
    """    
    playerCards = []
    dealerCards = []
    state = None
    stateHistory = []
    action = None
    dealerCard = None
    usableAce = False
    dealerState = None
    catchMe = True

    # Deal the cards
    drawnCard = drawCard()
    playerCards.append(drawnCard)
    
    drawnCard = drawCard()
    dealerCards.append(drawnCard)
    dealerCard = drawnCard

    drawnCard = drawCard()
    playerCards.append(drawnCard)

    drawnCard = drawCard()
    dealerCards.append(drawnCard)
    dealerState = sum(dealerCards)

    dealerCard = dealerCards[0]

    if 1 in playerCards:
        usableAce = True
    else:
        pass
    state = sum(playerCards), usableAce, dealerCard 

    while(1):
        action, current = epsGreedy(Q, state)
        if action == 0:
            stateHistory.append((current, 0))
            drawnCard = drawCard()
            playerCards.append(drawnCard)  
            if drawCard == 1:
                usableAce = True
            state = sum(playerCards), usableAce, dealerCard
            if state[0] > 21: 
                return -1, stateHistory, True
            else:
                pass
        else:
            stateHistory.append((current, 1))
            break 

    
    usableAce = False
    drawMore = True
    dealerState = sum(dealerCards)
    if dealerState >= current:
        catchMe = False

    for idx, card in enumerate(dealerCards):
        if card == 1:
            dealerCards[idx] = 11
            usableAce = True
            break

    if dealerState >= 17 and catchMe:
        drawMore = False
    else:
        pass
    
    while(drawMore):
        drawnCard = drawCard()
        if drawnCard == 1 and sum(dealerCards) < 11:
            dealerCards.append(11)
            usableAce = True
        elif drawnCard + sum(dealerCards) > 21 and usableAce == True:
            for idx, card in enumerate(dealerCards):
                if card == 11:
                    dealerCards[idx] = 1
                    usableAce = False
            dealerCards.append(drawnCard)
        else:
            dealerCards.append(drawnCard)

        dealerState = sum(dealerCards)
        if dealerState >= current:
            catchMe = True

        if dealerState >= 17 and catchMe:
            break
        elif dealerState >= 21:
            break
        else:
            continue
    
    if dealerState > 21:
        return 1, stateHistory, True
    elif dealerState == current:
        return 0, stateHistory, True
    elif current > dealerState:
        return 1, stateHistory, True
    elif current < dealerState:
        return -1, stateHistory, True
    else:
        return 0, stateHistory, True

# %% Update Q[]

def updateQ(Q, q, result):
    """Function for updating Q table

    Args:
        Q (list): Table of all states and played actions
        q (list): List of tuples, each tuple represents one state and action played in that state
        result (int): Result of played game. 1 if player won, -1 if dealer won, 0 if it's a tie

    Returns:
        [list]: Updated Q
    """    
    flag = False
    newState = []

    for state in q:
        currentState, move = state
        for currentQ in Q:
            if currentState == currentQ[0]:
                # Update HIT and HOLD moves
                if move == 0:
                    currentQ[1].append(result)
                    flag = True
                    break
                else:
                    currentQ[2].append(result)
                    flag = True
                    break
            else: pass

        if flag == False:
            # We dont have currentState in Q so we need to make a new one
            if move == 0:
                newState.append(currentState)
                newState.append([result])
                newState.append([])
            else:
                newState.append(currentState)
                newState.append([])
                newState.append([result])
            Q.append(newState)
            newState = []
        else: pass
        flag = False
    
    return Q


# %% Main

results = []
result = None
learningSum = 0
learningList = []

Q = [[4, [1], [-1]]]

for i in range(10000):
    result, history, valid = playGame(Q)    
    results.append(result)
    Q = updateQ(Q, history, result)
    print("Game: "+ str(i) + ', Result: ' +str(result))

print('-------------------------------------')    
for index,res in enumerate(results):
    if res == 0:
        results.remove(res)
print(sum(results)/len(results))
print('-------------------------------------')
print(len(results))

# %%
