import numpy as np
import random

############ EDIT ABOVE FUNCTIONS ####

def create_Q_table():  # create q table with zeros and size
    q_table = np.zeros('''FIX ME''')  # number of states, number of actions
    return q_table

def update(q_table, state, action, r, Gamma, stateNext, actionNext):
    # use formula to update q_table
    q_table[state][action] = '''FIX ME'''
    return q_table

def choose_action(state, q_table, epsilon):
    if '''FIX ME''': #  take a random number and compare to exploratio rate
        action = random.randint('''FIX ME''')  # choose a random action
    else:
        action = np.argmax('''FIX ME''') # choose the best action for a state
    return action

def reduce_epsilon(epsilon):

    epsilon = epsilon * '''FIX ME'''  # reduce epsilon after each step
    epsilon = max('''FIX ME''') # set a minimum value for epsilon
    return epsilon