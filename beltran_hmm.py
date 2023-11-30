import re

def markov():
    #read inputfile
    output = open("hmm.out", "w")
    datasets, markovvalues, observableVals, constants= readFile()
    numofSols = int(inputf.pop(0))
    for set in datasets:
        setconsts = solveConstants(set, markovvalues)
        output.write(set + "\n")

        for i in range(0, numofSols):
            start = 1
            f = 0
            line = inputf[i].rstrip()
            needed = getNeeded(line.rsplit(r' given '))
            if setconsts[0] != markovvalues[0][0]:
                start = 0
            if needed[1] != markovvalues[0]:
                f = 1

            solve = solveIter2(int(needed[0]), setconsts, start, markovvalues[0])
            obsConst = findObsConst(constants, observableVals.index(needed[2]), needed[1])
            sol = (obsConst*solve) / solveIterObs(constants, observableVals.index(needed[2]), solve, f)

            output.write(line + " = " + str(sol)+"\n")
    output.close()


def solveIterObs(const, index, solve, opp):
    #the solve being passed is the same as the first elem in const
    if opp != 0:
        solve = 1-solve
    sol = (float(const[0][1][index])*solve) + (float(const[1][1][index])*(1-solve))
    return sol

def solveIter2(iter, constants, start, markovvalue):
    for _ in range(0, iter):
        sol = constants[1]*start + constants[2]*(1-start)
        #(first elem | S)*(If S is start or not) + (other elem | T)*(1 - start)
        if markovvalue != constants[0]:
            #if first elem of markovvalues is not the same as the computed constants... then we subtract so we can keep solving the first
            start = 1 - sol
        else:
            start = sol

    if markovvalue != constants[0]:
        #if first elem of markovvalues is not the same as the computed constants... so we subtract
        return 1 - sol
    return sol

def findObsConst(constants, obs, markov):
    for e in constants:
        if markov == e[0]:
            num = e[1][obs]
            return float(num)

def readFile():
    global inputf
    num = int(inputf.pop(0))
    datasets = readDataSet(num)
    markovvalues = inputf.pop(0).rstrip().split(" ")
    observableValues = inputf.pop(0).rstrip().split(" ")
    constants = getConstants(markovvalues, datasets)

    return datasets, markovvalues, observableValues, constants

def readDataSet(numofsets):
    global inputf
    datasets = []
    for _ in range(0, numofsets):
        x = inputf.pop(0)
        datasets.append(x.rstrip())
    return datasets

def getConstants(markovvalues, datasets):
    global inputf
    newlist = []
    for value in markovvalues:
        pairvalues = []
        pairvalues.append(value)
        pairs = inputf.pop(0).rstrip().split(" ")
        pairvalues.append(pairs)
        newlist.append(pairvalues)
    return newlist

def solveConstants(data, markovvalues):
    firstelem = data[0]
    constants = [firstelem]
    for value in markovvalues:
        dataocc = data[:-1].count(value[0])
        count = 0 #contains number of occurence 
        for i in range(1, len(data)-1):
            if data[i+1] == value[0] and data[i] == firstelem:
                count += 1
        constants.append(count / dataocc)
    return constants

def getNeeded(line):
    ls = [line[0][-1]] #add the number
    for e in line:
        ls.append(e[:-1])
    return ls

inputfile = open("hmm.in", "r")
inputf = inputfile.readlines()
inputfile.close()


markov()