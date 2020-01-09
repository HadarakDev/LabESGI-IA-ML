import numpy as np
import random

############ EDIT ABOVE FUNCTIONS ####

def create_Q_table():  # create q table with zeros and size
    q_table = np.zeros((9, 4))  # number of states, number of actions
    return q_table

def update(q_table, state, action, r, Gamma, stateNext, actionNext):
    # use formula to update q_table
    q_table[state][action] += 0.85 * (r + Gamma * max(q_table[stateNext]) - q_table[state][action])
    return q_table

def choose_action(state, q_table, epsilon):
    if random.uniform(0, 1) < epsilon: #  take a random number and compare to exploratio rate
        action = random.randint(0, 3)  # choose a random action
    else:
        action = np.argmax(q_table[state,:])
    return action

def reduce_epsilon(epsilon):

    epsilon = epsilon * 0.995  # reduce epsilon after each step
    epsilon = max(epsilon, 0.5) # set a minimum value for epsilon
    return epsilon