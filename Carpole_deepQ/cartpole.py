import random
import gym
import numpy as np
from collections import deque
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from PIL import Image


BATCH_SIZE = 10
GAMMA = 0.80


def create_model(nb_input, nb_output):
    model = Sequential()
    model.add(Dense(24, input_dim=nb_input, activation="relu"))
    model.add(Dense(24, activation="relu"))
    model.add(Dense(nb_output, activation="linear"))
    model.compile(optimizer="adam", loss="mse")
    return model

def predict(model, state, action_space, explo_ratio):
    if np.random.rand() < explo_ratio:
        return random.randrange(action_space)
    return np.argmax(model.predict(state)[0])


def replay(model, memory, explo_ratio):
    if len(memory) < BATCH_SIZE:
        # not enough data to train
        return explo_ratio
    batch = random.sample(memory, BATCH_SIZE)

    for action, state, reward, state_next, done in batch:
        q_update = reward
        if not done:
            q_update = reward + GAMMA * np.argmax(model.predict(state_next)[0])
        q_values = model.predict(state)
        q_values[0][action] = q_update
        model.fit(state, q_values, verbose=0)
        explo_ratio = explo_ratio / (1/5)
        explo_ratio = max(explo_ratio, 0.05)
    return explo_ratio


if __name__ == "__main__":
    env = gym.make("CartPole-v1")
    observation_space = env.observation_space.shape[0]
    action_space = env.action_space.n
    model = create_model(observation_space, action_space)
    run = 0
    explo_ratio: float = 0.5
    while True:
        run += 1
        state = env.reset()
        state = np.reshape(state, [1, observation_space])
        print(state)

        step = 0  # init starting simulation step at zero
        memory = []
        print("nb run:" + str(run))
        while True:  # Each timestep within said simulation...
            step += 1
            env.render()

            action = predict(model, state, action_space, explo_ratio)
            state_next, reward, done, info = env.step(action)
            state_next = np.reshape(state_next, [1, observation_space])
            memory.append((action, state, reward, state_next, done))
            state = state_next

            if done:
                break
            # save model or print stuff
            explo_ratio = replay(model, memory, explo_ratio)

