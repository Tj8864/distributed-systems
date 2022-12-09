from time import sleep
import random

def nBitRandom(n):
    rand = random.randint(2**(n-1),(2**n)-1)
    if rand%2 == 0:
        rand+=1
    return rand


def millerRabin(candidate):
    maxDivisionsByTwo = 0
    evenComponent = candidate-1
   
    while evenComponent % 2 == 0:
        evenComponent >>= 1
        maxDivisionsByTwo += 1
    assert(2**maxDivisionsByTwo * evenComponent == candidate-1)
   
    def trialComposite(round_tester):
        if pow(round_tester, evenComponent, 
               candidate) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2**i * evenComponent, candidate) == candidate-1:
                return False
        return True
    numberOfRabinTrials = 20
    for i in range(numberOfRabinTrials):
        round_tester = random.randrange(2, candidate)
        if trialComposite(round_tester):
            return False
    return True

def findPrimes(primeCount):
    primes = []
    while len(primes) < primeCount:
        candidate = nBitRandom(256)
        if millerRabin(candidate):
            primes.append(candidate)
    return primes

if __name__ == "__main__":
    print(findPrimes(10))