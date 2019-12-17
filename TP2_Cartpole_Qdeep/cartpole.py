import random
import gym
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam


BATCH_SIZE = 10
GAMMA = 0.80


def create_model(nb_input, nb_output):
    model = Sequential()
    model.add(Dense(24, input_dim=nb_input, activation="relu"))
    model.add(Dense(24, activation="relu"))
    model.add(Dense(nb_output, activation="softmax"))
    model.compile(optimizer=Adam(lr=0.001), loss="mse")
    return model

def predict(model, state, action_space, explo_ratio):
    if np.random.rand() < explo_ratio:
        return random.randrange(action_space)
    return np.argmax(model.predict(state)[0])


def replay(model, memory, explo_ratio):
    if len(memory) < BATCH_SIZE:
        # not enough data to train
        return explo_ratio, model
    batch = random.sample(memory, BATCH_SIZE)

    for action, state, reward, state_next, done in batch:
        q_update = reward
        if not done:
            q_update = reward + GAMMA * np.amax(model.predict(state_next)[0])
        q_values = model.predict(state)
        q_values[0][action] = q_update
        model.fit(state, q_values, verbose=0)
        explo_ratio = explo_ratio * 0.95
        explo_ratio = max(explo_ratio, 0.05)
    return explo_ratio, model


if __name__ == "__main__":
    env = gym.make("CartPole-v1")
    observation_space = env.observation_space.shape[0]
    action_space = env.action_space.n
    model = create_model(observation_space, action_space)
    run = 0
    explo_ratio: float = 1
    max_steps = 0
    while True:
        run += 1
        state = env.reset()
        state = np.reshape(state, [1, observation_space])

        step = 0
        memory = []
        print("nb run:" + str(run))
        while True:
            step += 1
            env.render()

            action = predict(model, state, action_space, explo_ratio)
            state_next, reward, done, info = env.step(action)
            if done:
                reward = -reward

            state_next = np.reshape(state_next, [1, observation_space])
            memory.append((action, state, reward, state_next, done))
            state = state_next

            if done:
                if max_steps < step:
                    max_steps = step
                print("\t Model is done with steps: " + str(step) + " max steps: " + str(max_steps))
                break
            explo_ratio, model = replay(model, memory, explo_ratio)


