def fillRewards(gameMemory, totalScore, numGames):
   initialDf = .99
   averageScore = totalScore/numGames
   curScore = 0
   for i in range(len(gameMemory)):
      if gameMemory[i][2] > 0
         curScore = (gameMemory[i][2] - averageScore)/averageScore
      gameMemory[i][2] = curScore
      curScore *= initialDf

def calcReward(prevObservation, curObservation):
   stocksWon = 0
   stocksLost = 0
   percentWon = 0
   percentLost = 0

   stocksLost = prevObservation[5] - curObservation[5]
   stocksWon = prevObservation[5] - curObservation[5]
   percentLost = curObservation[4] - prevObservation[4]
   percentWon = curObservation[4+16] - prevObservation[4+16]

   return -1000*stocksLost + 1000*stocksWon - percentLost + percentWon


