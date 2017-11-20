def normalizeData(data):
    dataOut = []
    #distance = d/40
    dataOut.append(data[0]/40)
    index = 2
    for i in range(2):
        #x = x/85
        dataOut.append(data[index]/85)
        index += 1
        #no need for y
        #dataOut.append(data[index]/30)
        index += 1
        #no percent
        #dataOut.append(data[index]/40)
        index += 1
        #no stock
        #dataOut.append(data[index]/4)
        index += 1
        #facing
        if data[index] == 1:
            dataOut.append(data[index])
        else:
            dataOut.append(-1)
        index += 1
        #Action value = 1 if > 0x2c
        if data[index] >= 0x2c:
            dataOut.append(1)
        else:
            dataOut.append(-1)
        index += 1
        #action frame
        #dataOut.append(data[index]/10)
        index += 1
        #invuln
        #if data[index] == 1:
        #    dataOut.append(data[index])
        #else:
        #    dataOut.append(-1)
        index += 1
        #stun frames left
        dataOut.append((data[index] + data[index + 1])/30)
        index += 1
        #dataOut.append(data[index]/5)
        index += 1
        #charging smash
        #if data[index] == 1:
        #    dataOut.append(data[index])
        #else:
        #    dataOut.append(-1)
        index += 1
        #jumps = 1 if > 0
        if data[index] > 0:
            dataOut.append(1)
        else:
            dataOut.append(0)
        index += 1
        #on ground
        if data[index] == 1:
            dataOut.append(data[index])
        else:
            dataOut.append(-1)
        index += 1
        #x speed
        dataOut.append(data[index]/5)
        index += 1
        #y speed
        #dataOut.append(data[index]/3)
        index += 1
        #off stage
        if data[index] == 1:
            dataOut.append(data[index])
        else:
            dataOut.append(-1)
        index += 1
    return dataOut
