from random import *
from math import *
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
    return guess

def swapTest(guess, constraints, i, j):
    guess[j], guess[i] = guess[i], guess[j]
    k = tester(guess, constraints)
    guess[j], guess[i] = guess[i], guess[j]
    return k

def loopWithProb(guess, constraints):
    origSat = tester(guess, constraints)
    numTrys = len(constraints) / 100
    repeats = []
    changeInSat = {}
    for _ in range(numTrys):
	a = randint(0,len(guess)-1)
        b = randint(0,len(guess)-1)
        satisfiedAfterSwapping = swapTest(guess, constraints, a, b)
        changeInSat[(a,b)] = satisfiedAfterSwapping - origSat
    makeProbs(changeInSat)
    for swap, sat in changeInSat.items():
	for i in range(sat):
	    repeats.append(swap)
    selected = choice(repeats)
    guess[selected[0]], guess[selected[1]] = guess[selected[1]], guess[selected[0]]
    return tester(guess, constraints)

def makeProbs(changeInSat):
    smallest = abs(min(changeInSat.values()))
    for a,b in changeInSat.items():
	changeInSat[a] = (b + smallest) * (b + smallest)
    return changeInSat

	


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
    for _ in range(4):
	loopOnce(ret, constraints, wizzNames)
    while loopWithProb(ret, constraints) < len(constraints):
	print(loopWithProb(ret, constraints))
    

    print(ret)
    #print("--- %s seconds ---" % (time.time() - start_time))
    print((tester(ret, safety)))



def findFailed(guess, constraints):
    #guess is an array
    wrong = []
    for constraint in constraints:
        first = constraint[0]
        second = constraint[1]
        third = constraint[2]
        lower = min(guess.index(first), guess.index(second))
        upper = max(guess.index(first), guess.index(second))
        if guess.index(third) < lower or guess.index(third) > upper:
            pass
	else:
	    wrong.append(constraint)
    return wrong



def tester(guess, constraints):
    #guess is an array
    satisfied = 0
    for constraint in constraints:
        first = constraint[0]
        second = constraint[1]
        third = constraint[2]
        lower = min(guess.index(first), guess.index(second))
        upper = max(guess.index(first), guess.index(second))
        if guess.index(third) < lower or guess.index(third) > upper:
            satisfied += 1
    return satisfied
