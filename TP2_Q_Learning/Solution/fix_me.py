import numpy as np
import random

############ EDIT ABOVE FUNCTIONS ####

def create_Q_table():  # create q table with zeros and size
    q_table = np.zeros((9, 4))  # number of states, number of actions
    return q_table

def update(q_table, state, action, r, Gamma, stateNext, actionNext):
    q_table[state][action] = q_table[state][action] + 0.1 * (
                r + Gamma * q_table[stateNext][actionNext] - q_table[state][action])
    return q_table

def choose_action(state, q_table, epsilon):
    if np.random.rand() < epsilon:
        action = random.randint(0, 3)
    else:
        action = np.argmax(q_table[state])
    return action

def reduce_epsilon(epsilon):
    epsilon = epsilon * 0.995
    epsilon = max(epsilon, 0.40)
    return epsilon