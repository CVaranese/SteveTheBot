import gym
import math
import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense
from statistics import mean

env = gym.make("CartPole-v0")
env.reset()
goalSteps = 500
scoreReq = 75
initialGames = 10000

def getInitial():
    trainingData = []
    scores = []
    acceptedScores = []

    for episode in range(initialGames):
        score = 0
        gameMemory = []
        prevObservation = []
        observation = env.reset()
        for t in range(goalSteps):
            if episode < 5:
                env.render()
                pass
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)
            if len(prevObservation) > 0:
                gameMemory.append([prevObservation, action])
            prevObservation = observation
            score+= reward
            if done:
                break
        if score >= scoreReq:
            acceptedScores.append(score)
            for data in gameMemory:
                if data[1] == 1:
                    output = [0, 1]
                elif data[1] == 0:
                    output = [1, 0]
                trainingData.append([data[0], output])
        env.reset()
        scores.append(score)
    print("Average: " + str(mean(acceptedScores)))
    return trainingData

def trainModel(data, model):
    test = np.array(data)
    x = np.array([i[0] for i in data]).reshape(-1, len(data[0][0]))
    y = []
    for i in data:
        if i[1] == 0:
            y.append([1, 0])
        elif i[1] == 1:   
            y.append([0, 1])
    #mn = mean([i[2] for i in data])
    rewards = np.array([i[2] for i in data]) 
    #print(rewards)

    model.fit(x, y, sample_weight=rewards, epochs=3)
    return model

def main():

    np.set_printoptions(threshold=100000)
    newData = []
    model = Sequential()
    model.add(Dense(16, input_dim=4, activation='relu'))
    #model.add(Dense(16, activation='relu'))
    model.add(Dense(2, activation = 'sigmoid'))

    #model.compile(loss='categorical_crossentropy',
    #    optimizer='rmsprop')
    model.compile(loss='mse',
        optimizer='adam')

    env = gym.make('CartPole-v0')
    m1 = 0

    #trainingData = getInitial()
    #model = trainModel(trainingData, model)
    for x in range(1000):
        gameMemory = []
        scores = []
        acceptedScores = []
        newData = []
        for episode in range(200):
            score = 0
            observation = env.reset()
            for t in range(200):
                if episode < 10:
                    env.render()
                    pass
                #if len(prevObs) == 0:
                #    action = random.randrange(0, 2)
                prediction = model.predict(observation.reshape(-1,
                        len(observation)))
                if random.random() < math.exp(-1*x):
                    #print("random")
                    action = env.action_space.sample()
                else:
                    if (random.random() < prediction[0][0]):
                        action = 0
                    else:
                        action = 1
                    #action = np.argmax(model.predict(
                    #        observation.reshape(-1, len(observation))))
                gameMemory.append([observation, action, 0])
                observation, reward, done, info = env.step(action)
                score += reward
                if done:
                    #print("Episode {} finished after {} timesteps".format(episode, t+1))
                    gameMemory[len(gameMemory) - 1][2] = 1
                    break
            #if score >= scoreReq:
            #    acceptedScores.append(score)
            #    for data in gameMemory:
            #        if data[1] == 1:
            #            output = [0, 1]
            #        elif data[1] == 0:
            #            output = [1, 0]
            #        newData.append([data[0], output])
            scores.append(score)
        m1 = mean(scores)
        print("Average: " + str(m1))
        j = 0
        print(len(scores))
        allScores = []
        df = .98
        deg = df
        for i in range(len(gameMemory)):
            #allScores.append(scores[j]*df)
            change = False
            if gameMemory[i][2] == 1:
                change = True
            gameMemory[i][2] = (scores[j] - m1)*deg
            #print(gameMemory[i][2])
            #print("DF: " + str(deg))
            deg *= df
            if(change == True):
                j += 1
                deg = df
                change = False
        if(m1 < 195):
            model = trainModel(gameMemory, model)
        else:
            break

if __name__ == "__main__":
    main()
