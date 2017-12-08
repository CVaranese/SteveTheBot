#!/usr/bin/python3
import melee
import time
import keras
import math
import argparse
import signal
import rewards
import Utility
import sys
import train
import os.path
import dataFix
import Model
import random
import numpy as np
import loss
from pathlib import Path
from pynput.keyboard import Key, Controller

batchSize = 50
episodeLength = 10
actionsPerSecond = 30
df = .98
rewardN = 20
batchMemory = 10
#This example program demonstrates how to use the Melee API to run dolphin programatically,
#   setup controllers, and send button presses over to dolphin

def check_port(value):
    ivalue = int(value)
    if ivalue < 1 or ivalue > 4:
         raise argparse.ArgumentTypeError("%s is an invalid controller port. \
         Must be 1, 2, 3, or 4." % value)
    return ivalue

def signal_handler(signal, frame):
    dolphin.terminate()
    if args.debug:
        log.writelog()
        print("") #because the ^C will be on the terminal
        print("Log file created: " + log.filename)
    print("Shutting down cleanly...")
    if args.framerecord:
        framedata.saverecording()
    sys.exit(0)

def main():
    chain = None

    parser = argparse.ArgumentParser(description='Example of libmelee in action')
    parser.add_argument('--port', '-p', type=check_port,
                        help='The controller port your AI will play on',
                        default=2)
    parser.add_argument('--opponent', '-o', type=check_port,
                        help='The controller port the opponent will play on',
                        default=1)
    parser.add_argument('--debug', '-d', action='store_true',
                        help='Debug mode. Creates a CSV of all game state')
    parser.add_argument('--framerecord', '-r', default=False, action='store_true',
                        help='Records frame data from the match, stores into framedata.csv')
    parser.add_argument('model', type=str, default="Steve",
                        help='The file of the AI')

    args = parser.parse_args()

    log = None
    if args.debug:
        log = melee.logger.Logger()

    framedata = melee.framedata.FrameData(args.framerecord)
    opponent_type = melee.enums.ControllerType.UNPLUGGED

    #Create our Dolphin object. This will be the primary object that we will interface with
    dolphin = melee.dolphin.Dolphin(ai_port=args.port, opponent_port=args.opponent,
        opponent_type=opponent_type, logger=log)
    #Create our GameState object for the dolphin instance
    gamestate = melee.gamestate.GameState(dolphin)
    #Create our Controller object that we can press buttons on
    controller = melee.controller.Controller(port=args.port, dolphin=dolphin)
    keyboard = Controller()


    signal.signal(signal.SIGINT, signal_handler)

    #Run dolphin and render the output
    dolphin.run(render=True)

    #Plug our controller in
    #   Due to how named pipes work, this has to come AFTER running dolphin
    #   NOTE: If you're loading a movie file, don't connect the controller,
    #   dolphin will hang waiting for input and never receive it
    controller.connect()

    actorModel = []
    modelFile = Path("models/" + args.model + "/actor.h5")
    if modelFile.exists():
        actorModel = keras.models.load_model('models/' + args.model + "/actor.h5",
            custom_objects={'entropy_categorical_crossentropy': loss.entropy_categorical_crossentropy})
        #actorModel = keras.models.load_model('models/' + args.model + "/actor.h5")
    else:
        actorModel = Model.buildActorModel()
        actorModel.save('models/' + args.model + "/actor.h5")

    valueModel = []
    modelFile = Path("models/" + args.model + "/value.h5")
    if modelFile.exists():
        valueModel = keras.models.load_model('models/' + args.model + "/value.h5")
    else:
        valueModel = Model.buildValueModel()
        valueModel.save('models/' + args.model + "/value.h5")

    #Main loop
    numGames = 0
    allMemories = np.array([])
    prevObservation = []
    prevObs = []
    observation = []
    score = 0
    totalScore = []
    pickedCPU = 0
    firstStart = False
    stepNum = 0
    batchNum = 0
    fixedData = []
    First = True
    recordedMem =[]
    tempMem = []
    prediction = []
    episodeMemory = []
    episodeReward = 0
    curSave = 0
    loadState = False
    while True:
        gamestate.step() 
        stepNum += 1
        if stepNum >= 1000:
            print("Still Going!")
            stepNum = 0
        #What menu are we in?
        if gamestate.menu_state == melee.enums.Menu.IN_GAME:
            gamestate.step() 
            observation = gamestate.tolist()
            fixedObs = dataFix.normalizeData(observation)
            #print(fixedObs)

            #begin in-game loop
            #play should be in infinite time mode
            #play number of episodes, where an episode is a 10 second length of gametime
            #after the specified number, train agent
            for batch in range(batchSize):
                #episodes are x seconds * 30 frames per second
                for _ in range(episodeLength*30):

                    #every frame consists of:
                    #agent gives action
                    #agent receives reward
                    #agent receives next observation
                    
                    fixedObs = fixedObs.reshape(1, len(fixedObs))
                    #print("fixedObs: ",fixedObs)
                    action = actorModel.predict(fixedObs)
                    if _%30 == 0:
                        print("PREDICTION: ", action)
                    #find which move was predicted
                    #maxIndex = np.argmax(action, axis=1)[0]
                    maxIndex = np.random.choice(range(54), p=action[0])
                    #change to random move if necessary
                    #if random.random() < .05:#max(.02, math.exp((-.75)*(batchNum + 2.5))):
                    #    maxIndex = random.randint(0, 53)
                    #convert to categorical i.e. [0, 0, 0, 0, 1, 0, 0]
                    prediction = keras.utils.to_categorical(maxIndex,
                        num_classes=len(action[0]))
                    predictedReward = valueModel.predict(fixedObs)
                    predictedReward = predictedReward[0][0]
                    #print("PRED REWARD: ", predictedReward)
                    #print("New action!")
                    #press button
                    controller.flush()
                    button, stick = Utility.decide_action(maxIndex)
                    controller.simple_press(stick[0], stick[1], button)

                    #step through two frames, since we want to work 2 frames at a time
                    gamestate.step()
                    controller.flush()
                    prevObs = observation
                    observation = gamestate.tolist()
                    reward = rewards.calcReward(prevObs, observation)
                    gamestate.step()
                    controller.flush()
                    prevObs = observation
                    observation = gamestate.tolist()
                    reward += rewards.calcReward(prevObs, observation)
                    #keep track of total
                    episodeReward += reward

                    #record what happened
                    episodeMemory.append([fixedObs, prediction, reward, predictedReward, 0, 0])
                    #print("Pred Rew: ", predictedReward)
                    #print("Actual Rew: ", reward)
                    #print("\nMEM: ", episodeMemory[len(episodeMemory) - 1])
                    
                    #fix the data to a format we can use
                    fixedObs = dataFix.normalizeData(observation)

                    #end of one step

                #episode has ended
                #need to modify rewards so that the network knows what is good behavior
                totalScore.append(episodeReward)
                print("E Reward: ", episodeReward)
                print("Num: ", batch)
                curReward = episodeMemory[-1][3]
                episodeReward = 0
                for i in reversed(range(len(episodeMemory))):
                    ri = episodeMemory[i][2]
                    curReward += ri
                    #if i < len(episodeMemory) - rewardN:
                        #curReward -= episodeMemory[i+rewardN][2]*(df**(rewardN))
                        #episodeMemory[i][4] = curReward - (episodeMemory[i][3])
                            #episodeMemory[i + rewardN][3]*(df**(rewardN)))
                    #else:
                        #episodeMemory[i][4] += episodeMemory[len(episodeMemory) - 1][3]*(df**(len(episodeMemory) - 1 - i))
                        #episodeMemory[i][4] = curReward - (episodeMemory[i][3] -
                        #    episodeMemory[len(episodeMemory) - i][3]*(df**(len(episodeMemory) - i - 1)))
                    episodeMemory[i][4] += curReward - episodeMemory[i][3]
                    episodeMemory[i][5] = curReward
                    #episodeMemory[i][2] = curReward
                    #if i < len(episodeMemory) - 20:
                    #    episodeMemory[i][4] -= episodeMemory[i+20][2]*(df**20)
                    #print("INPUT: ", episodeMemory[i][0])
                    #print("REW: ", episodeMemory[i][2])
                    #print("CUR: ", episodeMemory[i][5])
                    print("PRED: ", episodeMemory[i][3])
                    #print("ADV: ", episodeMemory[i][4])
                    print()
                    curReward *= df
                    
                #loadState = True
                #actorModel = train.trainActorModel(episodeMemory, actorModel)
                #actorModel.save("models/" + args.model + "/actor.h5")
                #valueModel = train.trainValueModel(episodeMemory, valueModel)
                #valueModel.save("models/" + args.model + "/value.h5")
                #allMemories = np.array([])
                #totalScore = []

                #add this episode to our memory
                #print("EP MEM: ", episodeMemory)
                if len(allMemories) == 0:
                    allMemories = episodeMemory
                elif len(allMemories) <= batchSize*episodeLength*actionsPerSecond*batchMemory:
                    allMemories = np.append(allMemories, episodeMemory, axis=0)
                else:
                    allMemories = np.append(allMemories[batchSize*episodeLength*actionsPerSecond:],
                        episodeMemory, axis=0)
                #print("ALL MEMS: ", allMemories)
                episodeMemory = []

                #finished one episode processing

            #batch is done
            batchNum += 1
            print("LEN: ", len(allMemories))
            trainMems = allMemories[np.random.choice(allMemories.shape[0], allMemories.shape[0]//4, replace=False)]
            for mem in trainMems:
                mem[3] = valueModel.predict(mem[0])[0][0]
                mem[4] = mem[5] - mem[3]
            actorModel = train.trainActorModel(trainMems, actorModel)
            actorModel.save("models/" + args.model + "/actor.h5")
            #if batchNum % 200 == 0:
            #    valueModel = train.trainValueModel(trainMems, valueModel)
            #    valueModel.save("models/" + args.model + "/value.h5")
            #allMemories = np.array([])
            #totalScore = []

            '''
            tempReward = None
            prevObservation = observation
            observation = gamestate.tolist()
            fixedData = dataFix.normalizeData(observation)
            if len(prevObservation) > 0:
                score += rewards.calcReward(prevObservation, observation)
            if len(prediction) == 0:
                fixedData = np.append(fixedData, 
                    keras.utils.to_categorical(30))
            else:
                fixedData = np.append(fixedData, prediction)
            fixedArray = []
            for i in range(len(gameMemory) - 14, len(gameMemory)):
                if i < 0:
                    fixedArray.append(np.zeros(50))
                else:
                    fixedArray.append(gameMemory[i][0])
            fixedArray.append(fixedData)
            fixedArray = np.array(fixedArray).reshape(1, 15, 50)
            firstPrediction = model.predict(fixedArray)
            #firstPrediction = model.predict(np.array(fixedData).reshape(-1, 1, len(fixedData)))
            prediction = firstPrediction
            if stepNum == 999:
                print("Before Rand: ", prediction)
                print("OBS: ", fixedData)
                print("Random: ", batchNum, "num: ", math.exp(-.5 *(.25+batchNum)))

            gameMemory.append([(fixedData), 
                               (prediction),
                               tempReward])
            recordedMem.append([fixedData, firstPrediction, tempReward])
            if stepNum == 999:
                #print("CURGAMEMEM: ", gameMemory[len(gameMemory)-1])
                #print("FIRSTGAMEMEM: ", gameMemory[0])
                #print("SECONDGAMEMEM: ", gameMemory[1])
                print("After Rand: ", prediction)
                #pass
            
            #plug prediction in to move function
            '''

        #If we're at the character select screen, choose our character
        elif gamestate.menu_state == melee.enums.Menu.CHARACTER_SELECT:
            melee.menuhelper.choosecharacter(character=melee.enums.Character.CPTFALCON,
                gamestate=gamestate, controller=controller, swag=False, start=False)

        #If we're at the postgame scores screen, spam START
        #Postgame screen isnt relevant for out purposes right now
        elif gamestate.menu_state == melee.enums.Menu.POSTGAME_SCORES:
            '''
            firstStart = True
            if len(gameMemory) > 0:
               gameMemory[0][2] = score
               print("ADDED SCORE: ", score)
               print("GAME MEM: ", gameMemory[0])
               totalScore.append(score)
               print("SCORE: ", score)
               print("lenMemories: ", len(allMemories))
               # FIX FIX FIX (list of game memories) 
               print("NUM: ", numGames)
               if len(allMemories) == 0:
                   allMemories = gameMemory
               else:
                   allMemories = np.concatenate([allMemories, gameMemory], axis=0)
               print(allMemories[len(allMemories) - 1])
               gameMemory = []
               score = 0
               numGames += 1
               if numGames >= batchSize:
                  batchNum += 1
                  allMemories = rewards.fillRewards(allMemories, totalScore, numGames)
                  recordedMem = rewards.fillRewards(recordedMem, totalScore, numGames)
                  f = open('logs/batch' + str(batchNum) + '.txt', 'w+')
                  #for val in recordedMem:
                  #   f.write(str(val) + '\n')
                  #f.close()
                  model = train.trainModel(allMemories, model)
                  model.save("models/" + args.model)
                  numGames = 0
                  allMemories = np.array([])
                  prevObservation = []
                  recordedMem = []
                  observation = []
                  totalScore = []
            '''
            melee.menuhelper.skippostgame(controller=controller)

        #If we're at the stage select screen, choose a stage
        elif gamestate.menu_state == melee.enums.Menu.STAGE_SELECT:
            melee.menuhelper.choosestage(stage=melee.enums.Stage.FINAL_DESTINATION,
                gamestate=gamestate, controller=controller)
        #Flush any button presses queued up
        controller.flush()
        if log:
            log.logframe(gamestate)
            log.writeframe()

if __name__ == '__main__':
    main()
