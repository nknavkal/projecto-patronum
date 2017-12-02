import argparse
import numpy as np
import time
"""
======================================================================
  Complete the following function.
======================================================================
"""

def alphaTup(string1, string2):
    return tuple([min(string1, string2), max(string1, string2)])

def getPairs(constraints, wizards):
    appearsInPair = {}
    for name in wizards:
        appearsInPair[name] = 0
    for constraint in constraints:
        appearsInPair[constraint[0]] += 1
        appearsInPair[constraint[1]] += 1
    return appearsInPair


def addWizz(constraints, ordering, wizzMap, wizards, wizzToAdd):
    #finds out if there is a viable solution along this path
    ordering.append(wizzToAdd)
    if len(ordering) == len(wizzMap):
        return ordering
    wizards.remove(wizzToAdd)
    removed = []
    recentDeps = []
    i = 0
    while i < len(constraints):
        cons = constraints[i]
        if wizzToAdd == cons[0] or wizzToAdd == cons[1] or wizzToAdd == cons[2]:
            #if its in the 3rd space, constraint satisfied. If not, add it to dependencies, satisfy it later
            removed.append(cons)
            constraints.remove(cons)
            if cons[1] == wizzToAdd or cons[0] == wizzToAdd:
                if cons[1] != wizzToAdd:
                    wizzMap[cons[2]].addDep(cons[1])
                else:
                    wizzMap[cons[2]].addDep(cons[0])
                recentDeps.append(cons[2])
        else:
            i+=1



    inPair = getPairs(constraints, wizards)
    ret = -1
    #reverse if doing inThird
    for key, value in sorted(iter(inPair.items()), key=lambda k_v: (k_v[1],k_v[0])):
        depsSatisfied = True;
        for dep in wizzMap[key].deps:
            if (dep not in ordering):
                depsSatisfied = False
        if depsSatisfied:
            #check if viable solutions
            ret = addWizz(constraints, ordering, wizzMap, wizards, key)
            if ret != -1:
                break



    if ret == -1:
        #didn't find optimal ordering, undo changes from previos step
        ordering.pop()
        for cons in removed:
            constraints.append(cons)
        wizards.add(wizzToAdd)
        for wizz in recentDeps:
            wizzMap[wizz].removeLastDep()
    return ret



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


class Wizzrobe:
    def __init__(self, name):
        self.name = name
        self.deps = []
    def addDep(self, otherWizz):
        self.deps.append(otherWizz)
    def removeLastDep(self):
        self.deps.pop()


def getWizzMap(wizards):
    wizzMap = {}
    for wizz in wizards:
        wizzMap[wizz] = Wizzrobe(wizz)
    return wizzMap


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
    start_time = time.time()
    ret = 0
    ordering = []
    inPairs = getPairs(constraints, wizards)
    wizzMap = getWizzMap(wizards)
    

    for key, value in sorted(iter(inPairs.items()), key=lambda k_v1: (k_v1[1],k_v1[0])):
        ret = addWizz(constraints, ordering, wizzMap, set(wizards), key)
        if ret != -1:
            break
    print(ret)
    print("--- %s seconds ---" % (time.time() - start_time))
    print((tester(ret, constraints)))
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
