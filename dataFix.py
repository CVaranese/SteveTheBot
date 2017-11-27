import numpy as np
from keras import utils
def normalizeData(data):
    maxActions = 0x017E
    dataOut = np.array([])
    #Do not use distance or stage
    index = 2
    for i in range(2):
        #x = x/10
        dataOut = np.append(dataOut,data[index]*.1)
        index += 1
        #y = y/10
        dataOut = np.append(dataOut,data[index]*.1)
        index += 1
        #percent = percent/100
        dataOut = np.append(dataOut,data[index]*.01)
        index += 1
        #no stock since we're in infinite time
        #dataOut.append(data[index]/4)
        index += 1
        #facing -> -1 if left, 1 if right
        if data[index] == 1:
            dataOut = np.append(dataOut, 1)
        else:
            dataOut = np.append(dataOut, -1)
        index += 1
        #Action value = categorically encoded (max = maxActions)
        action = data[index]
        if action == 65535: #unknown action from dolphin for some reason
            action = maxActions + 1
        catAction = utils.to_categorical(action, maxActions+2)

        dataOut = np.append(dataOut, catAction)
        index += 1
        #action frame = frame*.02
        dataOut = np.append(dataOut,data[index]*.02)
        index += 1
        #invuln = 0 if no 1 if yes
        dataOut = np.append(dataOut,data[index])
        index += 1
        #hitlag frames left
        dataOut = np.append(dataOut,data[index]*.1)
        index += 1
        #hitstun frames left
        dataOut = np.append(dataOut,data[index]*.1)
        index += 1
        #charging smash, 0 if no 1 if yes
        dataOut = np.append(dataOut,data[index])
        index += 1
        #jumps
        dataOut = np.append(dataOut,data[index])
        index += 1
        #in air = 1 if yes 0 if no
        if data[index] == 1:
            dataOut = np.append(dataOut,0)
        else:
            dataOut = np.append(dataOut,1)
        index += 1
        #x speed
        dataOut = np.append(dataOut,data[index]*.5)
        index += 1
        #y speed
        dataOut = np.append(dataOut,data[index]*.5)
        index += 1
        #off stage = 1 if yes 0 if no
        if data[index] == 1:
            dataOut = np.append(dataOut,1)
        else:
            dataOut = np.append(dataOut,0)
        index += 1
    return dataOut
