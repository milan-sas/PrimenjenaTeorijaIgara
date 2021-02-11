import numpy as np
from numpy.random import rand, choice

def printPlay():
    print('\n')
    print(' '+ str(outputMatrix[0]) + ' | ' + str(outputMatrix[1]) + ' | ' + str(outputMatrix[2]) + ' ')
    print('-----------')
    print(' '+ str(outputMatrix[3]) + ' | ' + str(outputMatrix[4]) + ' | ' + str(outputMatrix[5]) + ' ')
    print('-----------')
    print(' '+ str(outputMatrix[6]) + ' | ' + str(outputMatrix[7]) + ' | ' + str(outputMatrix[8]) + ' ')
    print('\n')

def tryNotToLose():    
    for i in allPossib:
        temp = list(set(xplay).intersection(i))
        if len(temp)==2:
            tmp = str(set(i) ^ set(temp))
            tmp = int(tmp[1])
            if (tmp in xplay) or (tmp in oplay):
                return False
            else:
                print("O must play " + str(tmp) + "\n")
                oplay.append(tmp)
                outputMatrix[tmp-1] = 'O'
                return True
    return False

def tryToWin():
    for i in allPossib:
        temp = list(set(oplay).intersection(i))
        if len(temp)==2:
            tmp = str(set(i) ^ set(temp))
            tmp = int(tmp[1])
            if (tmp in xplay) or (tmp in oplay):
                return False
            else:
                oplay.append(tmp)
                outputMatrix[tmp-1] = 'O'
                return True
    return False

def justPlaySomething():
    temp = []
    for i in outputMatrix:
        try:
            temp.append(int(i))
        except:
            pass
    if len(temp)==0:
        print("The game has ended whith no winers\n")
        exit()
    elif len(temp)==1:        
        oplay.append(temp[0])
        outputMatrix[temp[0]-1] = 'O'
    else:
        play = choice(temp)
        oplay.append(play)
        outputMatrix[play-1] = 'O'
    print("O played "+ str(play) + "\n")

def didXWin():
    if len(xplay)>2:
        for i in allPossib:
            if (all(x in xplay for x in i)):
                return True
            else:
                continue
    else: return False

def checkInput():
    try:
        num = int(input())
        if (0 <= num <= 9):
            return num
        else:
            raise ValueError("Invalid valuem please choose valid value in range (1-9)")
    except Exception as identifier:
        print(Exception)
        print(identifier)
        return checkInput()

# All possible combiations for the WIN
allPossib = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
# Current state on board
outputMatrix = ['1', '2','3', '4', '5', '6', '7', '8', '9']
# List of X plays
xplay = []
# List of O plays
oplay = []

temp = []
tmp = None

printPlay()
# First play
print("Please choose place for X")
play = checkInput()
xplay.append(play)
outputMatrix[play-1] = 'X'

justPlaySomething()
printPlay()
# End of first play
while(1):
    print("Please choose place for X")
    play = None
    xplay.append(play)
    outputMatrix[play-1] = 'X'
    if didXWin():
        print("X Wins \n")
        print('X played:')
        print(xplay)
        print('O played:')
        print(oplay)
        printPlay()
        break
    elif tryToWin():
        print("O Wins \n")
        print('X played:')
        print(xplay)
        print('O played:')
        print(oplay)
        printPlay()
        break
    elif tryNotToLose():
        pass
    else: justPlaySomething()

    printPlay()

