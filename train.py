import numpy as np
import math
import tensorflow as tf

def create_dataset(dataset, look_back):
    data = []
    for i in range(len(dataset)):
        a = []
        for j in range(i - look_back + 1, i + 1):
            if j < 0:
                a.append(np.zeros(50))
            else:
                a.append(dataset[j])
        data.append(a)
    return np.array(data)


def trainActorModel(gameMemory, model):
   x = np.array([i[0] for i in gameMemory]).reshape(-1, len(gameMemory[0][0][0]))
   #xi = np.array([i[0] for i in gameMemory]).reshape(-1, len(gameMemory[0][0][0]))
   #xj = tf.stop_gradient(np.array([i[4] for i in gameMemory]).reshape(-1, len(gameMemory[0][0][0])))
   #x = xi * xj
   #x = np.array([i[0]*i[4] for i in gameMemory]).reshape(-1, len(gameMemory[0][0][0]))
   #x = create_dataset([i[0] for i in gameMemory], 15).reshape(-1, 15, 50)
   #y = tf.stop_gradient(np.array([i[1] * i[4] for i in gameMemory]))
   y = np.array([i[1] * i[4] for i in gameMemory])
   rewards = np.array([i[4] for i in gameMemory])

   print("ACTOR TRAINING")
   print("X: ")
   print(x)
   print("Y: ")
   print(y)
   print("REWARDS: ")
   print(rewards)

   #model.fit(x, y, sample_weight=rewards, epochs=5)
   model.fit(x, y, epochs=10)
   return model

def trainValueModel(gameMemory, model):
   x = np.array([i[0] for i in gameMemory]).reshape(-1, len(gameMemory[0][0][0]))
   #x = create_dataset([i[0] for i in gameMemory], 15).reshape(-1, 15, 50)
   y = np.array([i[5] for i in gameMemory])
   #rewards = np.array([(30*5 - 1 -i)%(30*5)/(30*5) for i in range(len(gameMemory))])
   #rewards = np.array([math.sqrt((30*10 - 1 -i)%(30*10)/(30*10)) for i in range(len(gameMemory))])


   print("VALUE TRAINING")
   print("X: ")
   print(x)
   print("Y: ")
   print(y)
   #print("REWARDX: ")
   #print(rewards)

   #model.fit(x, y, epochs=5, sample_weight=rewards)
   model.fit(x, y, epochs=5)
   return model
