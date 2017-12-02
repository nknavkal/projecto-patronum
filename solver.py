import argparse
import numpy as np
"""
======================================================================
  Complete the following function.
======================================================================
"""
import random
from math import *
from datetime import datetime
import sys
import glob
import errno
import time
import os
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
    j = 0
    for i in wizzNames:
        while j < 1:
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
            j += 1
    return tester(guess, constraints)

def swapTest(guess, constraints, i, j):
    guess[j], guess[i] = guess[i], guess[j]
    k = tester(guess, constraints)
    guess[j], guess[i] = guess[i], guess[j]
    return k

def loopWithProb(guess, constraints, temp):
    origSat = tester(guess, constraints)
    #a = random.randint(0,len(guess)-1)
    #b = random.randint(0,len(guess)-1)
    ###################
    aDict = {}
    aList = []
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
            #temp[0] = (len(constraints) - tester(guess, constraints))*1.0/len(constraints)

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
    origSat = tester(guess, constraints)
    #a = random.randint(0,len(guess)-1)
    #b = random.randint(0,len(guess)-1)
    ###################
    unsatSet = testUnsat(guess, constraints)
    sampleUnsat = random.choice(unsatSet)
    a, b, c = guess.index(sampleUnsat[0]), guess.index(sampleUnsat[1]), guess.index(sampleUnsat[2])
    adict = {}
    adict[(c, a)] = swapTest(guess, constraints, c, a)
    adict[(c, b)] = swapTest(guess, constraints, c, b)
    if adict[(c, a)] > adict[(c, b)]:
        optimal, suboptimal = (c, a), (c, b)
    else:
        optimal, suboptimal = (c, b), (c, a)
    #aList = [(c, a), (c, b)]
    if random.random() < temp[0]:
        key = suboptimal
    else:
        key = optimal
        #key = aList[1]
    value = adict[key]
    guess[key[0]], guess[key[1]] = guess[key[1]], guess[key[0]]
    print(tester(guess, constraints), temp[0])
    temp[0] *= .999
    return tester(guess, constraints)

def makeProbs(aDict):
    sum = 0
    min = 10000000000
    probDict = {}
    for k, v in aDict.items():
        sum += v
        if v < min:
            min = v
    for k, v in aDict.items():
        probDict[k] = pow((v + min + 1.0) / (sum + min + 1), 2)
    return probDict


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

def megaMain(path):
    #path = '/home/projecto-patronum/phase2_inputs/inputs20/*.in'
    #iles = os.listdir(path)
    for name in os.listdir(path): # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
        #start_time = time.time()
        print(path + name)
        main(path + name)
        print("--- %s seconds ---" % (time.time()))
    print("")

def main(fileName):
    start_time = time.time()
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
    print("--- %s seconds ---" % (time.time() - start_time))
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

def testUnsat(guess, constraints):
    passed = []
    failed = []
    for constraint in constraints:
        first = constraint[0]
        second = constraint[1]
        third = constraint[2]
        lower = min(guess.index(first), guess.index(second))
        upper = max(guess.index(first), guess.index(second))
        if guess.index(third) < lower or guess.index(third) > upper:
            passed.append(constraint)
        else:
            failed.append(constraint)
    return failed

def solve(num_wizards, num_constraints, wizards, constraints):
    """
    Write your algorithm here.
    Input:
        num_wizards: Number of wizards
        num_constraints: Number of constraints
        wizards: An array of wizard names, in no particular order
        constraints: A 2D-array of constraints,
                     where constraints[0] may take the form ['A', 'B', 'C']i

    Output:
        An array of wizard names in the ordering your algorithm returns
    """
    ret = np.random.choice(wizards, num_wizards, False).tolist()
    loopOnce(ret, constraints, wizards)
    temp = []
    temp.append(.3)
    start_time = time.time()
    while loopWithProb(ret, constraints, temp) < len(constraints):
        pass
        # this was to add a little more randomness
        # if time.time() - start_time > 60:
        #     a = random.randint(0, num_wizards)
        #     b = random.randint(0, num_wizards)
        #     c = random.randint(0, num_wizards)
        #     d = random.randint(0, num_wizards)
        #     e = random.randint(0, num_wizards)
        #     f = random.randint(0, num_wizards)
        #     ret[a], ret[b] = ret[b], ret[a]
        #     ret[c], ret[d] = ret[d], ret[c]
        #     ret[e], ret[f] = ret[f], ret[e]
    print(tester(ret, constraints))
    return ret

"""
======================================================================
   No need to change any code below this line
======================================================================
"""

def read_input(filename):
    with open(filename) as f:
        num_wizards = int(f.readline())
        num_constraints = int(f.readline())
        constraints = []
        wizards = set()
        for _ in range(num_constraints):
            c = f.readline().split()
            constraints.append(c)
            for w in c:
                wizards.add(w)

    wizards = list(wizards)
    return num_wizards, num_constraints, wizards, constraints

def write_output(filename, solution):
    with open(filename, "w") as f:
        for wizard in solution:
            f.write("{0} ".format(wizard))

if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "Constraint Solver.")
    parser.add_argument("input_file", type=str, help = "___.in")
    parser.add_argument("output_file", type=str, help = "___.out")
    args = parser.parse_args()

    num_wizards, num_constraints, wizards, constraints = read_input(args.input_file)
    solution = solve(num_wizards, num_constraints, wizards, constraints)
    write_output(args.output_file, solution)
