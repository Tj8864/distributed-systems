
from time import sleep
from random import randint

def runCompute():
    sleep(randint(5,10))
    primes = []
    for i in range(2,100):
        isPrime = True
        for j in range(2,i):
            if i%j == 0:
                isPrime = False
                break
        if isPrime:
            primes.append(i)
    
    return primes

def findPrimes(primeCount):
    primes = []
    while len(primes) < primeCount:
        candidate = randint(2,1000000)
        if(primeTest(candidate)):
            primes.append(candidate)
    return primes

def primeTest(num):
    for i in range(2,num):
        if num%i == 0:
            return False
        if i*i > num:
            break
    return True