import time

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


def addWizz(constraints, ordering, wizzMap, wizzNames, wizzToAdd, inThird):
    #finds out if there is a viable solution along this path
    ordering.append(wizzToAdd)
    if len(ordering) == len(wizzMap):
        return ordering
    wizzNames.remove(wizzToAdd)
    removed = set()
    recentDeps = []
    inThird_removed = inThird[wizzToAdd]
    i = 0
    while i < len(constraints):
        cons = constraints[i]
        if wizzToAdd == cons[0] or wizzToAdd == cons[1] or wizzToAdd == cons[2]:
            #if its in the 3rd space, constraint satisfied. If not, add it to dependencies, satisfy it later
            removed.add(cons)
            constraints.remove(cons)
            inThird[cons[0]] -= 1
            inThird[cons[1]] -= 1
            inThird[cons[2]] -= 1
            if cons[1] == wizzToAdd or cons[0] == wizzToAdd:
                if cons[1] != wizzToAdd:
                    wizzMap[cons[2]].addDep(cons[1])
                else:
                    wizzMap[cons[2]].addDep(cons[0])
                recentDeps.append(cons[2])
        else:
            i+=1

    #inThird = getThirds(constraints, wizzNames)
    ret = -1
    #reverse if doing inThird
    for key, value in sorted(iter(inThird.items()), key=lambda k_v: (k_v[1],k_v[0])):
        depsSatisfied = True;
        for dep in wizzMap[key].deps:
            if (dep not in ordering):
                depsSatisfied = False
        if depsSatisfied:
            #check if viable solutions
            ret = addWizz(constraints, ordering, wizzMap, wizzNames, key, inThird)
            if ret != -1:
                break

    if ret == -1:
        #didn't find optimal ordering, undo changes from previos step
        ordering.pop()
        for cons in removed:
            constraints.append(cons)
            inThird[cons[0]] += 1
            inThird[cons[1]] += 1
            inThird[cons[2]] += 1
        wizzNames.add(wizzToAdd)
        for wizz in recentDeps:
            wizzMap[wizz].removeLastDep()
    return ret

def getWizzNames(constraints, numNames):
    nameSet = set()
    for cons in constraints:
        nameSet.add(cons[0])
        nameSet.add(cons[1])
        nameSet.add(cons[2])
        if len(nameSet) == numNames:
            break
    return nameSet

def main(fileName):
    start_time = time.time()
    constraints, numNames = readFile(fileName)
    safety = constraints[:]
    ret = 0
    ordering = []
    wizzMap = {}
    wizzNames = getWizzNames(constraints, numNames)
    inThird = getThirds(constraints, wizzNames)



    for wizz in wizzNames:
        wizzMap[wizz] = Wizzrobe(wizz)
    #print(wizzMap)
    #reverse if doing inThird
    for key, value in sorted(iter(inThird.items()), key=lambda k_v1: (k_v1[1],k_v1[0])):
        ret = addWizz(constraints, ordering, wizzMap, wizzNames, key, inThird)
        if ret != -1:
            break
    print(ret)
    print("--- %s seconds ---" % (time.time() - start_time))
    print((tester(ret, safety)))





class Wizzrobe:
    def __init__(self, name):
        self.name = name
        self.deps = []
        self.numDeps = 0
    def addDep(self, otherWizz):
        self.deps.append(otherWizz)
        self.numDeps += 1
    def removeLastDep(self):
        self.deps.pop()
        self.numDeps -= 1




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
