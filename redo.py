import re

def markov():
    #read inputfile
    datasets, markovvalues, observableVals, constants= readFile()
    print("datasets: "+str(datasets))
    print("markovvalues: "+str(markovvalues))
    print("observable: "+str(observableVals))
    print("consts: "+str(constants))
    numofSols = int(inputf.pop(0))
    for set in datasets:
        setconsts = solveConstants(set, markovvalues)
        print(setconsts)

        for i in range(0, numofSols):
            start = 1
            f = 0
            line = inputf[i].rstrip()
            needed = getNeeded(line.rsplit(r' given '))
            print("needed: " + str(needed))
            if setconsts[0] != markovvalues[0][0]:
                start = 0
            if needed[1] != markovvalues[0]:
                print(needed[1])
                print(markovvalues[0])
                f = 1

            solve = solveIter2(int(needed[0]), setconsts, start, markovvalues[0])
            obsConst = findObsConst(constants, observableVals.index(needed[2]), needed[1])
            sol = (obsConst*solve) / solveIterObs(constants, observableVals.index(needed[2]), solve, f)
            print(str(obsConst)+"*"+str(solve)+"/"+str(solveIterObs(constants, observableVals.index(needed[2]), solve, f)))
            # print("solveIter: " + str(solveIter(int(needed[0]), setconsts, 1, opp)))

            print(line + " = " + str(sol))
            print("")


def solveIterObs(const, index, solve, opp):
    #the solve being passed is the same as the first elem in const
    if opp != 0:
        solve = 1-solve
    print("("+const[0][1][index]+"*"+str(solve) +")+(" + const[1][1][index] +"*"+str(1-solve)+")")
    sol = (float(const[0][1][index])*solve) + (float(const[1][1][index])*(1-solve))

    # if opp == 0:
    #     #means that the starting element in the set is the same as what's being asked
    #     print("("+const[0][1][index]+"*"+str(solve) +")+(" + const[1][1][index] +"*"+str(1-solve)+")")
    #     sol = (float(const[0][1][index])*solve) + (float(const[1][1][index])*(1-solve))
    # else:
    #     print("("+const[0][1][index]+"*"+str(1-solve) +")+(" + const[1][1][index] +"*"+str(solve)+")")
    #     sol = (float(const[0][1][index])*(1-solve)) + (float(const[1][1][index])*solve)
    return sol

def solveIter2(iter, constants, start, markovvalue):
    for _ in range(0, iter):
        # print(str(constants[1]) + "*"+str(start)+" + "+str(constants[2])+"*"+str(1-start))
        #start defines whether start is S or not
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
            # print("data[i]" + str(data[i]) + "  data[i+1]" + data[i+1] + " value: "+ value[0])
            if data[i+1] == value[0] and data[i] == firstelem:
                count += 1
        constants.append(count / dataocc)
        print("P("+firstelem + "|"+ value[0] +") = "+ str(count) + "/" + str(dataocc))
    return constants

def getNeeded(line):
    print(line)
    ls = [line[0][-1]] #add the number
    for e in line:
        ls.append(e[:-1])
    return ls

inputfile = open("hmm.in", "r")
inputf = inputfile.readlines()
inputfile.close()


markov()