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
    

    print(ret)
    #print("--- %s seconds ---" % (time.time() - start_time))
    print((tester(ret, safety)))







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
