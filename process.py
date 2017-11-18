

def readFile(inputFile):
    fileobj = open(inputFile, "r")
    print(fileobj.readlines())

def alphaTup(string1 string2):
    return tuple(min(string1, string2), max(string1, string2))

def makeOutsidePairs(fileArray):
    nameSet = set()
    outerSet = set()
    numWizards = int(fileArray[0])
    for i in range(2, fileArray.len):
        stringArr = i.split()
        for j in stringArr:
            outerSet.add(j)
        if len(nameSet) == numWizards:
            break
    for name1 in nameSet():
        for name2 in nameSet():
