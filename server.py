from _thread import *
from time import sleep
import socket
from instructions import Task, Instructions
from ast import literal_eval as listEval

instructions = {}
nodeConnections = {}
clientConnections = {}

def surveyNodes():
    aliveCount = 0
    for address in instructions.keys():
        nodeConnections[address].sendall("SURVERY".encode())
        data = nodeConnections[address].recv(2048).decode()
        if data == "ALIVE":
            aliveCount += 1
        else:
            instructions.pop(address)
            nodeConnections.pop(address)
    return aliveCount

def threaded_node(connection,address):
    while True:
        if len(instructions[address].taskQueue):
            task = instructions[address].taskQueue[0]
            print(f"Task {task} received from client {address}")
            connection.sendall(str.encode("CALCULATE "+str(task.count)+"\n"))
            data = connection.recv(1024*task.count).decode()
            print(data)
            if(data == "QUIT"):
                print(f"Connection with node {address} closed on receiving QUIT")
                break
            else:
                print("Gonna listEval: " + data)
                for prime in listEval(data):
                    task.returnList.append(prime)
                print(f"Task {task} completed by node {address}")
    connection.close()
    
def threaded_client(connection,address):
    global primesList
    while True:
        data = connection.recv(2048).decode()
        print(f"Data received from client {address}: "+data)
        if(data == "QUIT"):
            print(f"Connection with client {address} closed on receiving QUIT")
            break
        cnt = int(data.strip())
        aliveCnt = surveyNodes()
        cnt = (cnt+aliveCnt-1)//aliveCnt
        primes = []
        tasks = [Task(cnt) for i in range(aliveCnt)]
        i = 0
        for address in instructions.keys():
            instructions[address].taskQueue.append(tasks[i])
            print(f"Adding task {cnt} to node {address}")
            i = i+1
        for task in tasks:
            while(len(task.returnList) != cnt):
                pass
            for prime in task.returnList:
                primes.append(prime)
            instructions[address].taskQueue.pop(0)
        connection.sendall(str.encode(str(primes)))
    connection.close()

def server():
    config = open("server.txt","r")
    hostname, port = config.readline().split(" ")
    port = int(port)
    print(hostname,port)
    threads = []
    serverSocket = socket.socket()
    serverSocket.bind((hostname, port))
    
    serverSocket.listen(5)
    
    
    while True:
        conn,address = serverSocket.accept()
        role = conn.recv(1024).decode()
        if(role == "NODE"):
            print("Connection from node: " + str(address))
            nodeConnections[address] = conn
            instructions[address] = Instructions()
            start_new_thread(threaded_node, (conn,address))
        else:
            print("Connection from client: " + str(address))
            clientConnections[address] = conn
            start_new_thread(threaded_client, (conn,address))
    
    
if __name__ == "__main__":
    server()