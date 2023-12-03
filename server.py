import socket
import sys
import threading

# implement a keybind to shutdown the server in the future
class Server():
    
    # include strict types for inputs
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.connections = {}

    def start(self):
        # initialise TCP socket
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        serverSocket.bind(("", self.port))
        serverSocket.listen(5)
        print("The server is ready to receive")
        # keep looking for connection, then create new thread
        while True:
            connectionSocket, clientAddress = serverSocket.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(connectionSocket, clientAddress))
            client_handler.start()
        ## add message to confirm connection between server and client
        

    def handle_client(self, connectionSocket, clientAddress):
        # Display the username rather than the ip address
        print(f'{clientAddress} has connected to the server')
        #print(connectionSocket)
        self.connections[connectionSocket] = clientAddress
        # send a message to show connection from client
        while True:
            message = connectionSocket.recv(1024).decode()
            if not message:
                break

            print(message)
            # format the message 
            modifiedMessage = (f'{clientAddress[0]}: {message}')
                
            # send the message back to the all clients
            for connection in self.connections.keys():
                connection.send(modifiedMessage.encode())
            #connectionSocket.send(modifiedMessage.encode())
        
        # close the socket and remove the client from the list of connections
        connectionSocket.close()
        print(f'{clientAddress} has disconnected from the server')
        self.connections.pop(clientAddress[0])

# implement a function that handles commands, e.g. /msg <username> <message> 

if __name__=="__main__":
    #start_server()
    # create server instance, listening on port 8800
    server = Server('', int(sys.argv[1]))
    server.start()
