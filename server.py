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
    burned = []
    for address in instructions.keys():
        nodeConnections[address].sendall("SURVERY".encode())
        data = nodeConnections[address].recv(2048).decode()
        if data == "ALIVE":
            aliveCount += 1
        else:
            burned.append(address)
    for address in burned:
        instructions.pop(address)
        nodeConnections.pop(address)
    return aliveCount

def threaded_node(connection,address):
    while True:
        try:
            if not address in instructions:
                print(f"Connection with node {address} closed on receiving QUIT")
                break
            if len(instructions[address].taskQueue):
                task = instructions[address].taskQueue[0]
                instructions[address].taskQueue.pop(0)
                print(f"Task, count {task.count} sending to node {address}")
                connection.sendall(str.encode("CALCULATE "+str(task.count)+"\n"))
                data = connection.recv(2048*task.count).decode()
                print(f"Received result from {address}: "+data)
                if(data == "QUIT"):
                    instructions.pop(address)
                    nodeConnections.pop(address)
                    print(f"Connection with node {address} closed on receiving QUIT")
                    break
                else:
                    for prime in listEval(data):
                        task.returnList.append(prime)
                    print(f"Task {task} completed by node {address}")
        except ConnectionError:
            print(f"Connection with node {address} closed on connection error")
            break
        except KeyError:
            print(f"Connection with node {address} closed on receiving QUIT")
            break
    connection.close()
    
def threaded_client(connection,address):
    while True:
        data = connection.recv(2048).decode()
        if(data == "QUIT"):
            print(f"Connection with client {address} closed on receiving QUIT")
            break
        cnt = int(data.strip())
        aliveCnt = surveyNodes()
        if aliveCnt == 0:
            connection.sendall(str.encode("No compute nodes available, please try another time"))
            continue
        print(f"Task, count {cnt} received from client {address}, distributing to {aliveCnt} nodes")
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