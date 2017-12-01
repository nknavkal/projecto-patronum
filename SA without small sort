satisfiedAfterSwapping = swapTest(guess, constraints, a, b)

  if satisfiedAfterSwapping > origSat:
      guess[a], guess[b] = guess[b], guess[a]
      print(tester(guess, constraints), temp[0])
      if temp[0] > .1:
          temp[0] *= .999
      else:
        temp[0] = .3
      #temp[0] = (len(constraints) - tester(guess, constraints))*1.0/len(constraints)

  else:
      prob = exp((satisfiedAfterSwapping - origSat) * 1.0 / temp[0])
      x = random.random()
      if x < prob:
          guess[a], guess[b] = guess[b], guess[a]
          print(tester(guess, constraints), temp[0])
          if temp[0] > .1:
              temp[0] *= .999
          else:
              temp[0] = .3
        #temp[0] = (len(constraints) - tester(guess, constraints))*1.0/len(constraints)
      else:
          print("-")
  return tester(guess, constraints)
