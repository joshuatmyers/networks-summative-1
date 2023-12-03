import socket
import threading
import sys

# include strict typing
class Client():

    def __init__(self, username):
        # client ip and port
        self.name = username

    # include threads to allow for more connections
    # add message to confirm connection with server
    
    # create a new thread that just listens for messages from other users
    def connect(self, ip, port):

        # server ip and port  
        serverName = ip
        serverPort = port

        # initialise TCP socket
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to the server
        clientSocket.connect((serverName, serverPort))

        # start listening immediately - messages from other users
        #listen_thread = threading.Thread(target=self.listen, args=(clientSocket,))
        #listen_thread.start()

        while True:
            message = input("Message to send: ")

            if message == "close":
                message = ""
                clientSocket.send(message.encode())
                clientSocket.close()
                break

            message = f'{self.name} : ' + message

            # the socket address is the tuple that contains the ip and port
            clientSocket.send(message.encode())

            # this line allows the client to receive messages from the server, saving the message and address from the server
            data, serverAddress = clientSocket.recvfrom(1024)
            modifiedMessage = data.decode()
            print(modifiedMessage)
    
    def listen(self, connectionSocket):
        while True:
            data, serverAddress = connectionSocket.recvfrom(1024)
            modifiedMessage = data.decode()
            print(modifiedMessage)
        

if __name__ == "__main__":
    # python client.py "username" "hostname" "port"
    # add some checks with RE's to validate format
    client = Client(sys.argv[1])
    client.connect(str(sys.argv[2]), int(sys.argv[3]))

