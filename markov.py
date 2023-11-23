import re

def markov():
    global inputf
    num = int(inputf.pop(0))
    datasets = readDataSet(num) #get dataset here
    markovvalues = inputf.pop(0).rstrip().split(" ")
    observableValues = inputf.pop(0).rstrip().split(" ")
    markovvalues = getPairValues(markovvalues) #returns a list of [S, [P(E|S), P(F|S)]] and [T, [P(E|T), P(F|T)]]
    #given that the input values are in the same order as the observable values


    #next section should solve for it
    numOfSols = int(inputf.pop(0))
    for data in datasets:
        constants = getConstants(data, markovvalues)
        print(constants)
        for i in range(0, numOfSols):
            line = inputf[i].rstrip()
            needed = getNeeded(line.rsplit(r' given '), observableValues)
            #pass a line to a function that will solve for 
            
            #our constant value is stored in markov values
            #probability = (function to get constant value * (needed[0], needed[1])) / (needed[0], needed[2])
            # probability = (getInputConstant(markovvalues, needed[1], needed[2]) * finditer)
            print(markovvalues[needed[1]] + + observableValues[needed[2]])
            print("needed: " + str(needed))
            # print(line + " = ")

def readDataSet(numofsets):
    global inputf
    datasets = []
    for _ in range(0, numofsets):
        x = inputf.pop(0)
        datasets.append(x.rstrip())
    return datasets

# def iteratethrough(iter, prob, constants):
#     result = 0

def getConstants(data, markovvalues):
    firstelem = data[0]
    constants = [firstelem]
    for value in markovvalues:
        dataocc = data[:-1].count(value[0])
        count = 0 #contains number of occurence 
        for i in range(0, len(data)-1):
            # print("data[i]" + str(data[i]) + "  data[i+1]" + data[i+1] + " value: "+ value[0])
            if data[i] == value[0] and data[i+1] == firstelem:
                count += 1
        constants.append(count / dataocc)
        print("P("+firstelem + "|"+ value[0] +") = "+ str(count) + "/" + str(dataocc))
    return constants

def getNeeded(line, observableVals):
    ls = [line[0][-1]] #add the number
    for e in line:
        ls.append(observableVals.index(e[:-1]))
    return ls

def getPairValues(markovvalues):
    global inputf
    newlist = []
    for value in markovvalues:
        pairvalues = []
        pairvalues.append(value)
        pairs = inputf.pop(0).rstrip().split(" ")
        pairvalues.append(pairs)
        newlist.append(pairvalues)
    return newlist


inputfile = open("hmm.in", "r")
inputf = inputfile.readlines()
inputfile.close()


markov()
