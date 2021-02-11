# %% Define enviroment

from matplotlib.pyplot import title
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

def softmax(x):
    """Softmax decision policy:
        - Always choose bandit with highest probability -

    Args:
        x (list): Rewards for each bandit

    Returns:
        [int]: Index if selected bandit
    """    
    e_x = np.exp(x - np.max(x))
    ret = (e_x / e_x.sum())
    print(ret)
    return np.random.choice(range(len(x)), 1, p=ret)

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
# Defined list of bandits with mean and dev as touple
bandits = [(1, 1), (5, 10), (-3, 15),  (15, 2), (-24, 3)]
#Values of rewards for each bandit in first iteration
q = [1, 5, -3, 15, -24]

actions = []
rewards = []
# List of alla rewards for all bandits over time
qs = [q]
a = []

for k in range(1000):
    # body of the main loop
    a = softmax(q)
    print("Softmax policy returns the following list:")
    print(a)
    r = enviroment(a[0], bandits)
    q = learn(q, a[0], r)
    # logging actions
    actions.append(a[0])
    rewards.append(r)
    qs.append(q[:])

plt.plot(actions, '.', label='Actions')
plt.plot(rewards, '.', label='Rewards')
plt.legend()
plt.grid()

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
