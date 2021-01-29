import threading
import socket

# Connection Data
HOST = "127.0.0.1"
PORT = 55555

# Creating Server
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind((HOST, PORT))
SERVER.listen()

# Clients Data
CLIENTS = []
NICKNAMES = []


# Sending Messages To All Connected Clients
# Accepts a message as an argument and
# send the message to all clients.
def broadcast(message):
    for client in CLIENTS:
        client.send(message)


# Handling Messages From Clients
# Accepts a client as an argument
# and it will handle messages
# from that particular client.
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = CLIENTS.index(client)
            CLIENTS.remove(client)
            client.close()
            nickname = NICKNAMES[index]
            broadcast("{} left!".format(nickname).encode("ascii"))
            NICKNAMES.remove(nickname)
            break


# Receiving / Listening Function,
# It will accept Clients, ask for
# Nicknames, print and broadcast
# Nicknames and start Handling
# thread for client.
def receive():
    while True:
        # Accept Connection
        client, address = SERVER.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        NICKNAMES.append(nickname)
        CLIENTS.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode("ascii"))
        client.send("Connected to server!".encode("ascii"))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


if __name__ == "__main__":
    print("Server is listening...")
    receive()
