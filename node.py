import socket
import random
from compute import findPrimes
from time import sleep

def node():
    config = open("server.txt","r")
    hostname, port = config.readline().split(" ")
    port = int(port)
    
    nodeSocket = socket.socket()
    
    nodeSocket.connect((hostname, port))
    
    nodeSocket.send("NODE".encode())
    
    while True:
        try:
            data = nodeSocket.recv(2048).decode()
            if(data == "QUIT"):
                break
            if(data == "SURVERY"):
                print("Surveyed by server")
                nodeSocket.send("ALIVE".encode())
                continue
            primeCount = int(data.split(" ")[1])
            print(f"Received task {primeCount}")
            primes = findPrimes(primeCount)
            print(f"Sending primes {primes} to server")
            nodeSocket.send(str(primes).encode())
        except KeyboardInterrupt:
            print("Qutting")
            nodeSocket.send("QUIT".encode())
            break
node()