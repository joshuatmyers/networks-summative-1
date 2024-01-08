import socket
import threading
import sys

# include strict typing
class Client():

    def __init__(self, username):
        # client ip and port
        self.name = username
        self.socket = None

    # include threads to allow for more connections
    # add message to confirm connection with server
    
    # create a new thread that just listens for messages from other users
    def connect(self, ip, port):

        # server ip and port  
        serverName = ip
        serverPort = port

        # initialise TCP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to the server
        self.socket.connect((serverName, serverPort))

        # start listening immediately - messages from other users
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()

        sending_thread = threading.Thread(target=self.send)
        sending_thread.start()

    def send(self):
        while True:
            message = f'{str(sys.argv[1])}: {input("")}'
            self.socket.send(message.encode('utf-8'))    

    def listen(self):
        while True:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message == "?username":
                    self.socket.send(str(sys.argv[1]).encode('utf-8'))
                elif message == '?receivefile':
                    print("Receiving file...")
                    self.receivefile()
                    print("Recieved file!")
                elif message == '?sendfile':
                    print("User downloading a file")  
                    # prompt client to start listening for the file
                    self.socket.send('?receivefile'.encode('utf-8'))
                    # open the image to send
                    with open('test.jpg', 'rb') as file:
                        print("Sending to server")
                        self.sendFile(file)
                        print("Sending complete!")           
                    return 0
                else:
                    print(message)
            except ConnectionResetError:
                print("Connection closed by the server.")
                self.socket.close()
                break
            except Exception as e:
                print(f"Error: {e}")
                self.socket.close()
                break


    # join the threads after they have finished downloading
    def receivefile(self):
        try:
            with open('received_file.jpg', 'wb') as file:
                while True:
                    data = self.socket.recv(1024)
                    if not data:
                        break
                    file.write(data)
        except Exception as e:
            print(f"Error receiving file: {e}")
    
    def sendFile(self, file):
        # client sends file to the server
        print("User downloading a file")  
        # prompt client to start listening for the file
        self.socket.send('?receivefile'.encode('utf-8'))
        # open the image to send
        with open('test.jpg', 'rb') as file:
            print("Sending...")
            self.send_file(client, file)
            print("Sending complete!")           
        return 0
    
    """def listen(self, connectionSocket):
        while True:
            data, serverAddress = connectionSocket.recvfrom(1024)
            modifiedMessage = data.decode()
            print(modifiedMessage)"""

    """def send(self, connection_socket, message):
        connection_socket.send(message.encode())

    def input_handler(self, connection_socket):
        while True:
            message = input("Message to send: ")

            if message == "close":
                self.send(connection_socket, "")
                connection_socket.close()
                break

            message = f'{self.name} : ' + message
            self.send(connection_socket, message)
        """

    """def send(self, connectionsocket):
        while True:
            message = input("Message to send: ")

            if message == "close":
                message = ""
                connectionsocket.send(message.encode())
                connectionsocket.close()
                break

            message = f'{self.name} : ' + message

            # the socket address is the tuple that contains the ip and port
            connectionsocket.send(message.encode())

            # this line allows the client to receive messages from the server, saving the message and address from the server
            data, serverAddress = connectionsocket.recvfrom(1024)
            modifiedMessage = data.decode()
            print(modifiedMessage)"""
    
    
        

if __name__ == "__main__":
    # python client.py "username" "hostname" "port"
    # add some checks with RE's to validate format
    client = Client(sys.argv[1])
    client.connect(str(sys.argv[2]), int(sys.argv[3]))

