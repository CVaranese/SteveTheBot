import statistics
import numpy as np
def fillRewards(gameMemory, totalScore, numGames):
   initialDf = .9995
   minScore = min(totalScore)
   allScores = np.array(totalScore) - minScore
   allScores = (allScores - statistics.mean(allScores))/np.std(allScores)
   curScore = 0
   index = 0
   for i in range(len(gameMemory)):
      if gameMemory[i][2] != None:
         print("SCORE FOUND: ", gameMemory[i][2])
         curScore = allScores[index]
         index += 1
         #curScore = (gameMemory[i][2] - minScore)/abs(averageScore)
         print("CurScore: ", curScore)
      gameMemory[i][2] = curScore
      curScore *= initialDf
   return gameMemory

def calcReward(prevObservation, curObservation):
   stocksWon = 0
   stocksLost = 0
   percentWon = 0
   percentLost = 0

   if curObservation[7] <= 0x0A and prevObservation[7] > 0x0A:
      stocksLost += 1
   if curObservation[7+16] <= 0x0A and prevObservation[7+16] > 0x0A:
      stocksWon += 1
   #stocksLost = prevObservation[5] - curObservation[5]
   #stocksWon = prevObservation[5+16] - curObservation[5+16]
   if stocksLost > 0 or stocksWon > 0:
       return -1*stocksLost + 2*stocksWon
   percentLost = curObservation[4] - prevObservation[4]
   percentWon = curObservation[4+16] - prevObservation[4+16]
   if percentLost > 0 or percentWon > 0:
    return .03*percentWon - .01*percentLost
   return 0


