#def readFile(inputFile):
#    fileobj = open(inputFile, "r")
#    a = list(fileobj)
#    numNames = int(a[0].split()[0])
#    constraints = []
#    for i in a[2:]:
#        constraints.append(tuple(i.split()[:3]))
#    return constraints, numNames
#    #return(makeOutsidePairs(numNames, constraints))
#
#def alphaTup(string1, string2):
#    return tuple([min(string1, string2), max(string1, string2)])
#
#def getWizzNames(constraints, numNames):
#    nameSet = set()
#    for cons in constraints:
#        nameSet.add(cons[0])
#        nameSet.add(cons[1])
#        nameSet.add(cons[2])
#        if len(nameSet) == numNames:
#            break
#    return nameSet
#
#def getThirds(constraints, wizzNames):
#    appearsInThird = {}
#    for name in wizzNames:
#        appearsInThird[name] = 0
#    for constraint in constraints:
#        #switching to inPair
#        appearsInThird[constraint[0]] += 1
#        appearsInThird[constraint[1]] += 1
#        #appearsInThird[constraint[2]] += 1
#    return appearsInThird

def loopOnce(guess, constraints):
    bestCorrect = tester(guess)
    for i in wizzNames:
        bestIndex = 0
        iLocation = guess.index(i)
        for j in range(len(guess)):
            guess[j], guess[iLocation] = i, guess[j]
            k = tester(guess, constraints)
            if k > bestCorrect:
                bestCorrect = k
                bestIndex = j
            guess[j], guess[iLocation] = guess[iLocation], guess[j] 
