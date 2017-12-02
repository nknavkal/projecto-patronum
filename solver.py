import argparse
import numpy as np
"""
======================================================================
  Complete the following function.
======================================================================
"""
import random
from datetime import datetime

random.seed(datetime.now())


def alphaTup(string1, string2):
    return tuple([min(string1, string2), max(string1, string2)])

def numAppears(constraints, wizzNames):
    appearsInPair = {}
    for name in wizzNames:
        appearsInPair[name] = 0
    for constraint in constraints:
        appearsInPair[constraint[0]] += 1
        appearsInPair[constraint[1]] += 1
    return appearsInPair

def swapAll(guess, constraints, wizzNames):
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

def getOptAndSubOpt(guess, constraints, chosenCons):
    a = guess.index(chosenCons[0])
    b = guess.index(chosenCons[1])
    c = guess.index(chosenCons[2])

    caSatisfies = swapTest(guess, constraints, c, a)
    cbSatisfies = swapTest(guess, constraints, c, b)
    if caSatisfies > cbSatisfies:
        optimal, suboptimal = (c, a), (c, b)
    else:
        optimal, suboptimal = (c, b), (c, a)

    return optimal, suboptimal


def swapWithProb(guess, constraints, temp):
    origSat = tester(guess, constraints)

    unsatSet = getUnsat(guess, constraints)
    unsatToSwap = random.choice(unsatSet)
    
    optimal, suboptimal = getOptAndSubOpt(guess, constraints, unsatToSwap)

    if random.random() < temp[0]:
        key = suboptimal
    else:
        key = optimal

    guess[key[0]], guess[key[1]] = guess[key[1]], guess[key[0]]
    print(tester(guess, constraints), temp[0])
    if temp[0] > .0005:
	   temp[0] *= .999
    else:
	   temp[0] = .04
    return tester(guess, constraints)


def startingOrder(numAppears):
    a = []
    b = []
    for key, value in sorted(iter(numAppears.items()), key=lambda k_v1: (k_v1[1],k_v1[0])):
        a.append(key)
        temp = b
        b = a
        a = temp
    b.reverse()
    return a + b

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

def getUnsat(guess, constraints):
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
    ret = startingOrder(numAppears(constraints, wizards))
    swapAll(ret, constraints, wizards)
    temp = [.3]
    while swapWithProb(ret, constraints, temp) < len(constraints):
        pass

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
