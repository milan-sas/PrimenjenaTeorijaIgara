# %% Define enviroment

from matplotlib.pyplot import plot
import numpy as np
from numpy.random import rand, randint
import matplotlib.pyplot as plt

np.random.random()

def enviroment(a, bandits):
    """Defines reward for selected bandit
    Arguments:
        a (int) : Selected bandit
        bandits (list) : Sist of all bandits

    Returns:
        [float]: Reward for selected bandit
    """ 
    # Making shure that we selected the avaliable bandit
    assert (0 <= a < len(bandits))
    # Mean and deviation of selected bandit
    mean, dev = bandits[a]
    # Returning award that is mean + (-1,1) * deviation
    return mean + (rand()*2-1) * dev

# %% Decision policy

def greedy(q):
    """Greedy decision policy:
        - Choose bandit with highest reward -

    Args:
        q (list): Rewards for each bandit

    Returns:
        int : Index of bandit with highest reward
    """    
    return np.argmax(q)

def eps_greedy(q, eps=0.1):
    """EPS Greedy decision policy:
        - Choose bandit based on generated number and EPS -
        - If random generated number is lower than EPS chose random bandit -
        - Else choose bandit with highest reward -

    Args:
        q (list): Rewards for each bandit
        eps (float, optional): EPS parameter. Defaults to 0.1.

    Returns:
        [type]: Index if selected bandit
    """    
    if rand() < eps:
        # choose random action
        return randint(0, len(q))
    else:
        return greedy(q)

# %% Learning algorithm

def learn(q,a,r, p=0.9):    
    """Learning function

    Args:
        q (list): List of rewards for each bandit
        a (int): Action, which bandit is selected
        r (float): Reward for selected bandit
        p (float, optional): Defines how previous choices infuence current state. Defaults to 0.9.

    Returns:
        list : Updated rewards for each bandit
    """    
    # Making shure that we selected the avaliable bandit
    assert (0 <= a < len(bandits))
    # q novo = p * q staro + (1-p)*r
    q[a] = p * q[a] + (1-p) * r
    return q

# %% Main loop -- Learning and acting
# Defined list of bandits with mean and dev as list 
bandits = [[1, 1], [5, 10], [-3, 15],  [15, 2], [-24, 3]]
#Values of rewards for each bandit in first iteration
q = [1, 5, -3, 15, -24]

actions = []
rewards = []
# List of alla rewards for all bandits over time
qs = [q]
# One plot with 5 subplots for each bandit
fig,  axs = plt.subplots(5)

for tmp in range(1,6):
    # Changing EPS valus in range (0.1 , 0.5)
    epsilon = tmp/10
    print('--------------------------')
    print("Epsilon = " + str(epsilon))
    # Reseting bandits for each new EPS
    bandits = [[1, 1], [5, 10], [-3, 15],  [15, 2], [-24, 3]]
    for k in range(1000):
        # body of the main loop
        a = eps_greedy(q, eps=epsilon)
        r = enviroment(a, bandits)
        q = learn(q, a, r)
        # logging actions
        actions.append(a)
        rewards.append(r)
        qs.append(q[:])
        if k in [200, 400, 600, 800]:
            for band in bandits:
                # Change bandits mean in range (-50, 50)
                band[0] = round(rand()*100-50)
            print('New set of bandits for EPS = ' + str(epsilon) + ', k = ' + str(k) + ':')
            print(bandits) 

    axs[tmp-1].plot(actions, '.')
    axs[tmp-1].set_title("Epsilon = " + str(epsilon))

# %% Plotting 

q0 = [q[0] for q in qs]
q1 = [q[1] for q in qs]
q2 = [q[2] for q in qs]
q3 = [q[3] for q in qs]
q4 = [q[4] for q in qs]

plt.plot(q0, 'b', label="Q0")
plt.plot(q1, 'r', label="Q1")
plt.plot(q2, 'g', label="Q2")
plt.plot(q3, 'k', label="Q3")
plt.plot(q4, 'm', label="Q4")
plt.legend()
plt.grid()
# %%
