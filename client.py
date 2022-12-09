import socket

def client():
    config = open("server.txt","r")
    hostname, port = config.readline().split(" ")
    port = int(port)
    threads = []
    clientSocket = socket.socket()
    clientSocket.connect((hostname, port))
    clientSocket.send("CLIENT".encode())
    
    while True:
        print("Enter the required number of primes or QUIT if you want to leave: ")
        ip = input()
        if(ip == "QUIT"):
            clientSocket.send(ip.encode())
            break
        clientSocket.send(ip.encode())
        print("Data recieved from prime server: " + clientSocket.recv(1024*int(ip)).decode())
        
    
    
if __name__ == "__main__":
    client()