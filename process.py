

def readFile(inputFile):
    fileobj = open(inputFile, "r")
    a = list(fileobj)
    numNames = int(a[0].split()[0])
    numConstraints = int(a[1].split()[0])
    constraints = []
    for i in a[2:]:
        constraints.append(i.split()[:3])
    #print(constraints)
    return(makeOutsidePairs(numNames, constraints))

def alphaTup(string1, string2):
    return tuple([min(string1, string2), max(string1, string2)])

def makeOutsidePairs(numNames, constraints):
    nameSet = set()
    outerSet = set()
    for constraint in constraints:
        for element in constraint:
            nameSet.add(element)
        if len(nameSet) == numNames:
            break
    for name1 in nameSet:
        for name2 in nameSet:
            outerSet.add(alphaTup(name1, name2))
    print(outerSet)
