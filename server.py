import socket

def start_server():
    # server listens to port 8800 for client to connect to
    serverPort = 8800
    # initialise a TCP socket - TCP is defined with 'SOCK_STREAM'
    # AF_INET refers to the ipv4 address
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    
    
    serverSocket.bind(("", serverPort))
    print("The server is ready to receive")
    while True: 
        message, clientAddress = serverSocket.recvfrom(1024)
        # modifies the message to be all uppercase
        modifiedMessage = message.decode().upper() 
        # send the message back to the client
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)

if __name__=="__main__":
    start_server()