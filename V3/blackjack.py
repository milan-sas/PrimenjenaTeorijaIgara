# %% Define

import numpy as np
from numpy.random import rand, randint
import matplotlib.pyplot as plt


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

def epsGreedy(Q, state, eps = 0.1):
    hitMoves = []
    holdMoves = []
    currentSum, ace, dealer = state
    if ace and currentSum <= 11:
        currentSum += 10
    if currentSum == 21:
        return 1, currentSum
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
        if dealer < 7 and currentSum < 17:
            return 0, currentSum
        arr = np.array(Q)
        res = np.where(arr == currentSum)
        try:
            hitMoves = Q[res[0][0]][1]
            holdMoves = Q[res[0][0]][2]
            if sum(hitMoves) >= sum(holdMoves):
                return 0, currentSum
            else:
                return 1, currentSum
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

    if 1 in playerCards:
        usableAce = True
    else:
        pass
    # Starting sum of cards in player hands
    # if usableAce:
    #     for idx, item in enumerate(playerCards):
    #         if 1 == item:
    #             playerCards[idx] = 11
    #         else:
    #             pass
    state = sum(playerCards), usableAce, dealerCard 
    # History of states and actions

    while(1):
        action, current = epsGreedy(Q, state)
        if action == 0:
            stateHistory.append((current, 0))
            drawnCard = drawCard()
            playerCards.append(drawnCard)  
            if drawCard == 1:
                usableAce = True
            state = sum(playerCards), usableAce, dealerCard
            # if state[0] > 21 and usableAce:
            #     for idx, item in enumerate(playerCards):
            #         if 11 == item:
            #             playerCards[idx] = 1
            #             usableAce == False
            #         else:
            #             pass
            if state[0] >= 21: 
                break
            else:
                pass
        else:
            stateHistory.append((current, 1))
            break 

    #   while (state < 17):
    #         stateHistory.append((state, 0))
    #         drawnCard = drawCard()
    #         playerCards.append(drawnCard)
    #         state = sum(playerCards)
    #     stateHistory.append((state, 1))   
    # Last move is always HOLD  

    while (sum(dealerCards) < 17):
        drawnCard = drawCard()
        dealerCards.append(drawnCard)
        dealerState = sum(dealerCards)
    
    if sum(dealerCards) > 21:
        return 1, stateHistory, True
    elif sum(dealerCards) == current:
        return 0, stateHistory, True
    elif sum(dealerCards) == 21:
        return -1, stateHistory, False
    elif current > sum(dealerCards):
        return 1, stateHistory, True
    elif current < sum(dealerCards):
        return -1, stateHistory, True
    else:
        return 0, stateHistory, True
# %% Update Q[]

def updateQ(Q, q, result, alfpha=1):
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
                # if move == 0 and state != q[-1]:
                #     # HIT move
                #     currentQ[1].append(1)
                #     flag = True
                #     break
                # elif move == 0 and state == q[-1]:
                #     currentQ[1].append(result)
                #     flag = True
                #     break
                # elif move == 1 and state != q[-1]:
                #     # HOLD move
                #     currentQ[2].append(1)
                #     flag = True
                #     break
                # else:
                #     # HOLD move
                #     currentQ[2].append(result)
                #     flag = True
                #     break
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
            # if move == 0 and state != q[-1]:
            #     newState.append(currentState)
            #     newState.append([1])
            #     newState.append([])
            # elif move == 0 and state == q[-1]:
            #     newState.append(currentState)
            #     newState.append([result])
            #     newState.append([])
            # elif move == 1 and state != q[-1]:
            #     newState.append(currentState)
            #     newState.append([])
            #     newState.append([1])
            # else:
            #     newState.append(currentState)
            #     newState.append([])
            #     newState.append([result])
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

# Warm up play
Q = [[4, [1], [-1]]]

for i in range(10000):
    result, history, valid = playGame(Q)    
    results.append(result)
    Q = updateQ(Q, history, result)

# out = []
# print(results)
# print('-------------------------------------')
# print(Q)
# print('-------------------------------------')
# print(sum(results)/len(results))
# print('\nReal play\n')
# print(sum(results)/len(results))
# Now we play using Q (accumulated knowledge)

# for i in range(10000):
#     result, history, valid = playGame(Q) 
#     results.append(result)
#     if valid:
#         Q = updateQ(Q, history, result)
#     else:      
#         Q = updateQ(Q, history, (-1*result))

    for temp in range(50):
        try:            
            learningSum += results[-temp]
        except:
            break

    print("Game: "+ str(i) + ', Result: ' +str(result) + ', Learning sum of last 50 games: ' + str(learningSum))
    learningList.append(learningSum)
    learningSum = 0
    # print("Game: "+ str(i) + ', Result: ' +str(result))
# print(results)
# print('-------------------------------------')
# print(Q)
print('-------------------------------------')
# num = 0
# # If game finished with 0 (tie) then remove game from total score
# for r in results:
#     if r == 0:
#         results.remove(r)
#         num += 1
    
print(sum(results)/len(results))
print('-------------------------------------')
# print(len(results))
# print(num)

plt.plot(learningList)


# %%
