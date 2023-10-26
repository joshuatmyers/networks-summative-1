import socket

def start_client():
    serverName = "127.0.0.1"
    serverPort = 8800
    # initialise TCP socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    message = input("Input lowercase sentence: ")

    # the socket address is the tuple that contains the ip and port
    clientSocket.sendto(message.encode(), (serverName, serverPort))

    # this line allows the client to receive messages from the server, saving the message and address from the server
    modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
    print(modifiedMessage.decode())
    clientSocket.close()

if __name__ == "__main__":
    start_client()
