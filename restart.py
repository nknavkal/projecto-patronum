import random
from math import *
from datetime import datetime
random.seed(datetime.now())
def readFile(inputFile):
    fileobj = open(inputFile, "r")
    a = list(fileobj)
    numNames = int(a[0].split()[0])
    constraints = []
    for i in a[2:]:
        constraints.append(tuple(i.split()[:3]))
    return constraints, numNames
    #return(makeOutsidePairs(numNames, constraints))

def alphaTup(string1, string2):
    return tuple([min(string1, string2), max(string1, string2)])

def getThirds(constraints, wizzNames):
    appearsInThird = {}
    for name in wizzNames:
        appearsInThird[name] = 0
    for constraint in constraints:
        #switching to inPair
        appearsInThird[constraint[0]] += 1
        appearsInThird[constraint[1]] += 1
        #appearsInThird[constraint[2]] += 1
    return appearsInThird

def loopOnce(guess, constraints, wizzNames):
    bestCorrect = tester(guess, constraints)
    for i in wizzNames:
        iLocation = guess.index(i)
        bestIndex = iLocation
        for j in range(len(guess)):
            guess[j], guess[iLocation] = i, guess[j]
            k = tester(guess, constraints)
            if k > bestCorrect:
                bestCorrect = k
                bestIndex = j
                if k == len(constraints):
                    break
            guess[j], guess[iLocation] = guess[iLocation], guess[j]
        guess[bestIndex], guess[iLocation] = i, guess[bestIndex]
    return tester(guess, constraints)

def swapTest(guess, constraints, i, j):
    guess[j], guess[i] = guess[i], guess[j]
    k = len(constraints) - len(tester(guess, constraints))
    guess[j], guess[i] = guess[i], guess[j]
    return k

def loopWithProb_iterwizz(guess, constraints, temp):
    unSat = tester(guess, constraints)
    a = random.randint(0,len(guess)-1)
    b = random.randint(0,len(guess)-1)
    ###################
    unSat_choice = random.sample(tester, 1)
    a, b, c = unSat_choice[0], unSat_choice[1], unSat_choice[2]
    aDict = {}
    aDict[(c, a)] = swapTest(guess, constraints, c, a)
    aDict[(c, b)] = swapTest(guess, constraints, c, b)
    for i in range (4):
        a = random.randint(0,len(guess)-1)
        b = random.randint(0,len(guess)-1)
        aDict[(a,b)] = swapTest(guess, constraints, a, b)
    for key, value in sorted(iter(aDict.items()), key=lambda k_v1: (k_v1[1],k_v1[0]), reverse = True):
        if value > origSat:
            guess[key[0]], guess[key[1]] = guess[key[1]], guess[key[0]]
            print(tester(guess, constraints), temp[0])
            if temp[0] > .1:
                temp[0] *= .998
            else:
                temp[0] = .3
            #temp[0] = (len(constraints) - tester(guess, constraints))*1.0/len(c[onstraints)

        else:
            prob = exp((value - origSat) * 0.99 / temp[0])
            x = random.random()
            if x < prob:
                guess[key[0]], guess[key[1]] = guess[key[1]], guess[key[0]]
                print(tester(guess, constraints), temp[0])
                if temp[0] > .1:
                    temp[0] *= .998
                else:
                    temp[0] = .3
                #temp[0] = (len(constraints) - tester(guess, constraints))*1.0/len(constraints)
            else:
                print("-")
        return tester(guess, constraints)



#####################

def loopWithProb(guess, constraints, temp):
    unSat = tester(guess, constraints)
    #a = random.randint(0,len(guess)-1)
    #b = random.randint(0,len(guess)-1)
    ###################
    unSat_choice = random.choice(unSat)
    a, b, c = guess.index(unSat_choice[0]), guess.index(unSat_choice[1]),guess.index(unSat_choice[2])
    aDict = {}
    aDict[(c, a)] = swapTest(guess, constraints, c, a)
    aDict[(c, b)] = swapTest(guess, constraints, c, b)
    for key, value in sorted(iter(aDict.items()), key=lambda k_v1: (k_v1[1],k_v1[0]), reverse = True):
        if value > origSat:
            guess[key[0]], guess[key[1]] = guess[key[1]], guess[key[0]]
            #print(len(constraints) - len(tester(guess, constraints)), temp[0])
            if temp[0] > .1:
                temp[0] *= .998
            else:
                temp[0] = .3
            #temp[0] = (len(constraints) - tester(guess, constraints))*1.0/len(c[onstraints)

        else:
            prob = exp((value - origSat) * 0.99 / temp[0])
            x = random.random()
            if x < prob:
                guess[key[0]], guess[key[1]] = guess[key[1]], guess[key[0]]
                #print(tester(guess, constraints), temp[0])
                if temp[0] > .1:
                    temp[0] *= .998
                else:
                    temp[0] = .3
                #temp[0] = (len(constraints) - tester(guess, constraints))*1.0/len(constraints)
            else:
                print("-")
        return len(constraints) - len(tester(guess, constraints))


def getWizzNames(constraints, numNames):
    nameSet = set()
    for cons in constraints:
        nameSet.add(cons[0])
        nameSet.add(cons[1])
        nameSet.add(cons[2])
        if len(nameSet) == numNames:
            break
    return nameSet

def startingOrder(inThird):
    a = []
    b = []
    for key, value in sorted(iter(inThird.items()), key=lambda k_v1: (k_v1[1],k_v1[0])):
        a.append(key)
        temp = b
        b = a
        a = temp
    b.reverse()
    return a + b

def main(fileName):
    #start_time = time.time()
    constraints, numNames = readFile(fileName)
    safety = constraints[:]
    ret = 0
    #ordering = []
    wizzNames = getWizzNames(constraints, numNames)
    inThird = getThirds(constraints, wizzNames)

    ret = startingOrder(inThird)
    for _ in range(2):
        print(loopOnce(ret, constraints, wizzNames))
    temp = []
    temp.append(.5)
    while loopWithProb(ret, constraints, temp) < len(constraints):
        pass


    print(ret)
    #print("--- %s seconds ---" % (time.time() - start_time))
    #print((tester(ret, safety)))



def tester(guess, constraints):
    #guess is an array
    satisfied = 0
    unsatList = []
    for constraint in constraints:
        first = constraint[0]
        second = constraint[1]
        third = constraint[2]
        lower = min(guess.index(first), guess.index(second))
        upper = max(guess.index(first), guess.index(second))
        if guess.index(third) < lower or guess.index(third) > upper:
            satisfied += 1
        else:
            unsatList += constraint
    print(satisfied)
    return unsatList
