from keras.models import Sequential
from keras.layers import Dense, Reshape
from keras.optimizers import Adam
from keras.utils.np_utils import to_categorical
from collections import deque
import numpy as np

import sys

class Model:
    def __init__(self):
        learning_rate = 0.01
        state_size    = 7 * 7 * 3
        action_size   = 27
        hidden_size   = 64

        self.model = Sequential()
        self.model.add(Dense(hidden_size, activation='relu', input_dim=state_size))
        self.model.add(Dense(hidden_size, activation='relu', input_dim=state_size))
        self.model.add(Dense(action_size, activation='softmax'))
        self.optimizer = Adam(lr=learning_rate)
        self.model.compile(loss='mse', optimizer=self.optimizer)
        self.model.summary()

    def replay(self, memory, batch_size, gamma, target_model):
        inputs     = np.zeros((batch_size, 7 * 7 * 3))
        outputs    = np.zeros((batch_size, 27))
        mini_batch = memory.sample(batch_size)

        for i, (state, action, reward, next_state) in enumerate(mini_batch):
            inputs[i:i + 1] = state
            target          = reward

            if not (next_state == np.zeros(state.shape)).all():
                q = self.model.predict(next_state.reshape(1, 7 * 7 * 3))[0].argmax()
                next_action = np.argmax(q)
                target = reward + gamma * target_model.model.predict(next_state.reshape(1, 7 * 7 * 3))[0][next_action]

            outputs[i] = self.model.predict(state.reshape(1, 7 * 7 * 3))
            outputs[i][action.argmax()] = target

        self.model.fit(inputs, outputs, epochs=1, verbose=0)

class Memory:
    def __init__(self):
        self.buffer = deque()

    def add(self, exp):
        self.buffer.append(exp)

    def sample(self, batch_size):
        indice = np.random.choice(np.arange(len(self.buffer)), size=batch_size, replace=False)
        return [self.buffer[i] for i in indice]

class Agent:
    def get_action(self, state, epoch, main_model):
        epsilon = 0.001 + 0.9 / (1.0 + epoch)

        if epsilon < np.random.uniform(0, 1):
            action = main_model.model.predict(state.reshape(1, 7 * 7 * 3))[0].argmax()
        else:
            action = np.random.choice([i for i in range(27)])

        return to_categorical(action, 27)

if __name__ == '__main__':
    N_EPOCHS = 1000
    S_BATCH  = 4
    GAMMA    = 0.99

    args = sys.argv

