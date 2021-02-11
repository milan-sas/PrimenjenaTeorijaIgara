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
        
        if hitMoves > holdMoves:
            return 0, currentSum
        elif hitMoves > holdMoves:
            return 1, currentSum
        else:
            return 0, currentSum

# %% Play One Game with Monte Carlo

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
        return -1, stateHistory, False
    else:
        return 0, stateHistory, True

# %% Update Q[] by SARSA

def updateQSARSA(Q, q, result):
    """Function for updating Q table

    Args:
        Q (list): Table of all states and played actions
        q (list): List of tuples, each tuple represents one state and action played in that state
        result (int): Result of played game. 1 if player won, -1 if dealer won, 0 if it's a tie

    Returns:
        [list]: Updated Q
    """ 
    # Alfa i gama parametri 
    alpha = 0.1
    gamma = 0.9  

    '''
    Proveravamo da li je trenutno stanje terminalno stanje
    zato sto je blacjack takva igra da ja azuriranje podatak mogu da radim
    na kraju partije, umesto posle svakog poteza, zato sto sam 100% siguran da mi se dva stanja nece
    ponoviti u jednoj partiji
    '''
    for counter in range(len(q)):
        if counter == len(q)-1:
            # Terminal state
            newState = result
        else:
            # Uzimam sledece stanje koje koristim za azuriranje
            newState, newMove = q[counter+1]
        # Uzimam trenutno stanje za azuriranje
        currentState, move = q[counter]

        # Trazim trenutno stanje u Q tabeli
        for currentQ in Q:
            # Tasao sam trenutno stanje u tabeli
            if currentState == currentQ[0]:
                # Ako je HIT potez
                if move == 1:
                    # Azururanje vrednosti HIT poteza za currentState
                    currentQ[1] = currentQ[1] + alpha*(result + gamma*newState - currentQ[1])
                # Ako je HOLD potez
                else:
                    # Azururanje vrednosti HOLD poteza za currentState
                    currentQ[2] = currentQ[2] + alpha*(result + gamma*newState - currentQ[2])
    return Q

# %% Update Q[] by QLearning

def updateQLearning(Q, q, result):
    """Function for updating Q table

    Args:
        Q (list): Table of all states and played actions
        q (list): List of tuples, each tuple represents one state and action played in that state
        result (int): Result of played game. 1 if player won, -1 if dealer won, 0 if it's a tie

    Returns:
        [list]: Updated Q
    """  
    # Alfa i gama parametri
    alpha = 0.1
    gamma = 0.9  

    '''
    Proveravamo da li je trenutno stanje terminalno stanje
    zato sto je blacjack takva igra da ja azuriranje podatak mogu da radim
    na kraju partije, umesto posle svakog poteza, zato sto sam 100% siguran da mi se dva stanja nece
    ponoviti u jednoj partiji
    '''
    for counter in range(len(q)):
        if counter == len(q)-1:
            # Terminal state, value of new state if we used greedy policy
            '''
            Ako sam u terminalnom stanju partije, znaci da sam u tom stanju igrao hold
            a pretpostvka kojojm se vodim jeste da bi eventualno sledece
            stanje bilo kada ja odigram hit potez bilo +5 na trenutno stanje,
            odnosno da bi izvukao kartu br 5 sto ce mi u najvecem broju slucajeva
            znaciti da sam prebacio 21
            '''
            newState = q[counter][0] + 5
        else:
            '''
            Sledece stanje je ujedno i najbolje stanje zato 
            sto ga svakako biram greddy delom eps politike.
            Ako sam ga izabrao pomocu eps dela politike onda
            opet mog da gledam da li mi je dao HIT ili HOLD potez.
            Ako je HIT, sto je ovaj slucaj, onda je to zapravo proizvod
            greedy politike, ako je HOLD potez onda je to stanje koje
            je obradjeno u prethodnom delu koda
            '''
            newState, newMove = q[counter+1]
        # uzimam trenutno stanje da ga azuriram u politici
        currentState, move = q[counter]

        # Trazim trenutno stanje u Q tabeli
        for currentQ in Q:
            # nasao sam trenutno stanje u Q tabeli
            if currentState == currentQ[0]:
                # Move based on greedy policy
                '''
                Ovo je prekopiran deo koda za greedy politiku,
                jednostavo proveravam da li je vrednost za HIT potez
                veca od vrednosti za hold potez.
                Rezultat je proizvod greedy politike
                '''
                if currentQ[1] >= currentQ[2]:
                    currentQ[1] = currentQ[1] + alpha*(result + gamma*newState - currentQ[1])
                else:
                    currentQ[2] = currentQ[2] + alpha*(result + gamma*newState - currentQ[2])
                break
       

    return Q
# %% Main

prevRes = 0
currentRes = 0
balanceSARSA = 0
balanceQLearning = 0
f = open('result2.txt', 'a')
for m in range(100):
    resultsSARSA = []
    result = None

    Q = [[4,1,1],[5,1,1],[6,1,1],[7,1,1],[8,1,1],[9,1,1],[10,1,1],[11,1,1],[12,1,1],[13,1,1],[14,1,1],[15,1,1],[16,1,1],[17,1,1],[18,1,1],[19,1,1],[20,1,1],[21,1,1]]

    for i in range(20000):
        result, history, valid = playGame(Q) 
        resultsSARSA.append(result)
        Q = updateQSARSA(Q, history, result)
        print("Game: "+ str(i) + ', Result: ' +str(result))
        currentRes = sum(resultsSARSA)/len(resultsSARSA)
        if abs(prevRes - currentRes) > 0.001:
            balanceSARSA = i
        prevRes = currentRes

    resultsQLearning = []
    result = None
    learningSum = 0
    learningList = []
    prevRes = 0

    Q = [[4,1,1],[5,1,1],[6,1,1],[7,1,1],[8,1,1],[9,1,1],[10,1,1],[11,1,1],[12,1,1],[13,1,1],[14,1,1],[15,1,1],[16,1,1],[17,1,1],[18,1,1],[19,1,1],[20,1,1],[21,1,1]]

    for i in range(20000):
        result, history, valid = playGame(Q) 
        resultsQLearning.append(result)
        Q = updateQLearning(Q, history, result)
        print("Game: "+ str(i) + ', Result: ' +str(result))
        currentRes = sum(resultsQLearning)/len(resultsQLearning)
        if abs(prevRes - currentRes) > 0.001:
            balanceQLearning = i
        prevRes = currentRes


    
    print('-------------------------------------')    
    print('SARSA')  
    for index,res in enumerate(resultsSARSA):
        if res == 0:
            resultsSARSA.remove(res)
    print(sum(resultsSARSA)/len(resultsSARSA))
    print('Radna tacka: ' + str(balanceSARSA))
    print('-------------------------------------')

    print('-------------------------------------')  
    print('QLearning')  
    for index,res in enumerate(resultsQLearning):
        if res == 0:
            resultsQLearning.remove(res)
    print(sum(resultsQLearning)/len(resultsQLearning))
    print('Radna tacka: ' + str(balanceQLearning))
    print('-------------------------------------')

    f.write('Iteracija: ' + str(m) + '\n')
    f.write('SARSA: ' + str(sum(resultsSARSA)/len(resultsSARSA)) + '\n')
    f.write('Radna tacka postignuta u iteraciji: ' + str(balanceSARSA) + '\n')
    f.write('QLearning: ' + str(sum(resultsQLearning)/len(resultsQLearning)) + '\n')
    f.write('Radna tacka postignuta u iteraciji: ' + str(balanceQLearning)+ '\n')
    f.write('----------------------------' + '\n')

f.close()
# %%
