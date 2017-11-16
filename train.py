import numpy as np

def trainModel(gameMemory, model):
   x = np.array([i[0] for i in gameMemory]).reshape(-1, len(gameMemory[0][0]))
   y = np.array([i[1] for i in gameMemory])
   rewards = np.array([i[2] for i in gameMemory])

   model.fit(x, y, sample_weight=rewards, epochs=1)
   return model
