import socket
import sys
import threading
import logging
import time

# configure logging
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# implement a keybind to shutdown the server in the future
class Server():
    
    # include strict types for inputs
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = None
        self.connections = {}

    def setup(self):
        # initialise TCP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.socket.bind(("", self.port))
        self.socket.listen()
        self.start()

    def start(self):  
        # keep looking for connection, then create new thread
        print("The server is ready to receive")
        while True:
            connectionSocket, clientAddress = self.socket.accept()
            print(f'{clientAddress} has connected to the server')
            # add to connections
            self.connections[connectionSocket] = (clientAddress, None)
            # recieve username from client
            connectionSocket.send('?username'.encode('utf-8'))
            username = connectionSocket.recv(1024)
            print(f'The alias of this client is {username}')
            # add username to the connections dictionary
            self.connections[connectionSocket] = (clientAddress, username)
            self.send_all(f'{username} has connected to the server'.encode('utf-8'))
            connectionSocket.send("You are now connected!".encode('utf-8'))

            client_handler = threading.Thread(target=self.handle_client, args=(connectionSocket,))
            client_handler.start()
        
            
    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024)
                if message.decode('utf-8').split()[-1] == "?leave":
                    print("Leaving")                    
                    return 0
                if message.decode('utf-8').split()[-1] == "?download":
                    print("User downloading a file")  
                    # prompt client to start listening for the file
                    client.send('?receivefile'.encode('utf-8'))
                    # open the image to send
                    with open('test.jpg', 'rb') as file:
                        print("Sending...")
                        self.send_file(client, file)
                        print("Sending complete!")           
                    return 0
                if message.decode('utf-8').split()[-1] == "?sendfile":
                    # download data from client
                    print("Receiving file...")
                    self.receive_file()
                    print("Recieved file!")

                if message.decode('utf-8').split()[-1] == "?listconnections":
                    for k, v in self.connections.items():
                        print(k, v)
                if message.decode('utf-8').split()[-1] == "?pm":
                    # in the format ?pm user msg
                    # find user from connections
                    # send the message to the specific user
                    # indicate who the message is from and that it is a pm               
                    return 0
            
                self.send_all(message)
            except:
                ## remove client from connections
                print("removing client from connections")
                client.send('?username'.encode('utf-8'))
                username = client.recv(1024)
                del self.connections[client]
                client.close()
                self.send_all(f'{username} has left the chat room!'.encode('utf-8'))
                break   

    # Below will be all the command related functions of the server
            
    def pm(self):
        # private messaging function
        return 0

    def receive_file(self):
        # when users upload files to the server, they will be stored locally in the project files
        # assign the file a uid
        try:
            with open('fromClient.jpg', 'wb') as file:
                while True:
                    data = self.socket.recv(1024)
                    if not data:
                        break
                    file.write(data)
        except Exception as e:
            print(f"Error receiving file: {e}")
    
    def send_file(self, client, file):
        # when a user requests a file, the server must first check whether the item exists
        print("More sending")
        while True:
            data = file.read(1024)  # Adjust the chunk size as needed
            if not data:
                break
            client.send(data)
    
    def listfiles(self):
        # list all files - uid and description possibly
        return 0
    """   
    # clientAddress - (ip, unique port)

    def handle_client(self, connectionSocket, clientAddress):
        try:
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
                modifiedMessage = (f'\n{clientAddress[0]}: {message}')

                # log the information
                # add additional info when other commands are implemented
                logging.info(modifiedMessage)
                    
                # send the message back to the all clients
                for connection in self.connections.keys():
                    connection.send(modifiedMessage.encode())
                
            
            # close the socket and remove the client from the list of connections
            connectionSocket.close()
            print(f'{clientAddress} has disconnected from the server')
            self.connections.pop(clientAddress[0])
        except Exception as e:
            print(f"Error in client handler: {e}")
        finally:
            # Ensure the connection is closed even in case of an exception
            connectionSocket.close()
            print(f'{clientAddress} has disconnected from the server')
            self.connections.pop(clientAddress[0], None)
"""

    def send_all(self, message):
        # send the message back to the all clients
        for connection in self.connections:
            connection.send(message)

            

# implement a function that handles commands, e.g. /msg <username> <message> 

if __name__=="__main__":
    #start_server()
    # create server instance, listening on port 8800
    server = Server('', int(sys.argv[1]))
    server.setup()
