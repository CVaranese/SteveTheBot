import keras
from keras.models import Sequential
from keras.layers import Dense
from numpy import np

# length of outputs = 31
# length of inputs = 34


def main():

    np.set_printoptions(threshold=100000)
    model = Sequential()
    model.add(Dense(18, input_dim=34, activation='relu'))
    model.add(Dense(18, activation='relu'))
    model.add(Dense(31, activation = 'sigmoid'))

    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
    model.compile(loss='mse', optimizer='adam')
    return model
