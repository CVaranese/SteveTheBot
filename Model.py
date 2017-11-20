import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers.core import Dropout

# length of outputs = 31
# length of inputs = 32


def buildModel():
    model = Sequential()
    model.add(Dense(64, input_dim=17))
    model.add(Dropout(.4))
    #model.add(Dense(256, activation='relu'))
    #model.add(Dropout(.4))
    model.add(Dense(31, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam')
    print("WEIGHTS: ", model.get_weights())
    return model
