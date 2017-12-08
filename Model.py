import keras
from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.layers import LSTM
import loss
from keras.layers.core import Dropout
from keras.layers.advanced_activations import LeakyReLU


# length of outputs = 31
# length of inputs = 32


def buildActorModel():
    model = Sequential()
    model.add(Dense(128, input_dim=796, kernel_initializer='RandomUniform',
        bias_initializer='RandomUniform'))
    model.add(keras.layers.LeakyReLU())
    model.add(Dropout(.7))
    model.add(Dense(128, kernel_initializer='RandomUniform',
        bias_initializer='RandomUniform'))
    #model.add(LSTM(32, input_shape=(15, 50), kernel_initializer='RandomUniform',
    #    bias_initializer='RandomUniform'))
    model.add(Dropout(.7))
    #model.add(Dense(256, activation='relu'))
    #model.add(Dropout(.4))
    model.add(Dense(54, activation='softmax'))

    model.compile(loss=loss.entropy_categorical_crossentropy,
                  optimizer=keras.optimizers.Adam(lr=.0005, epsilon=.02, clipvalue=1e-4),
                  metrics=[keras.metrics.categorical_accuracy])
    #model.compile(loss='categorical_crossentropy',
    #              optimizer=keras.optimizers.Adam(lr=.001, epsilon=.02),
    #              metrics=[keras.metrics.categorical_accuracy])
    return model

def buildValueModel():
    model = Sequential()
    model.add(Dense(128, input_dim=796, kernel_initializer='RandomUniform',
        bias_initializer='RandomUniform'))
    model.add(keras.layers.LeakyReLU())
    model.add(Dropout(.8))
    model.add(Dense(128, kernel_initializer='RandomUniform',
        bias_initializer='RandomUniform', activation='sigmoid'))
    model.add(Dropout(.8))
    model.add(Dense(1))
    model.compile(loss='mse', optimizer='adam',
        metrics=['accuracy'])
    return model

