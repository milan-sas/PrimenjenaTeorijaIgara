# %% Define enviroment

import numpy as np
from numpy.random import rand, randint
import matplotlib.pyplot as plt

np.random.random()

#bandits = [(1, 1), (5, 10), (-3, 15),  (15, 2), (-24, 3)]


def enviroment(a, bandits):
    assert 0 <= a < len(bandits)
    mean, dev = bandits[a]
    return mean + (rand()*2-1) * dev

# %% Decision policy


def greedy(q):
    # if len(q) == 0:
    #     return -1
    # elif len(q) == 1:
    #     return 0
    # else:
    #     maxval = q[0]
    #     maxindex = 0
    #     for i in range(1, len(q)):
    #         if maxval < q[i]:
    #             maxval = q[i]
    #             maxindex = i
    #     return maxindex
    return np.argmax(q)

def eps_greedy(q, eps=0.1):
    if rand() < eps:
        # choose random action
        return randint(0, len(q))
    else:
        return greedy(q)

greedy([1, 2])

# %% Learning algorithm

def learn(q,a,r, p=0.9):
        # q novo = p * q staro + (1-p)*r
        assert 0 <= a < len(bandits)
        q[a] = p * q[a] + (1-p) * r
        return q

q = [1, 2, 3, 4, 5]
learn(q, 1, 102, 0.5)

# %% Main loop -- Learning and acting

bandits = [(1, 1), (5, 10), (-3, 15),  (15, 2), (-24, 3)]
#q = [0 for b in bandits]
q = [1, 5, -3, 15, 24]

actions = []
rewards = []
qs = []

for k in range(1000):
    # body of the main loop
    a = eps_greedy(q)
    r = enviroment(a, bandits)
    q = learn(q, a, r)
    # logging actions
    actions.append(a)
    rewards.append(r)
    qs.append(q)

plt.plot(actions, '.')

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
