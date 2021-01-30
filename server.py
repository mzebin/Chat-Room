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
BANNED_USERS = []
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
            # Recieving Messages
            message = client.recv(1024)

            # Checking for commands and Broadcasting Messages
            if message.decode("ascii").startswith("KICK"):
                username = message.decode("ascii").replace("KICK ", "")
                if username in NICKNAMES:
                    kick(username)
                else:
                    client.send("CMDERROR".encode("ascii"))
            elif message.decode("ascii").startswith("BAN"):
                username = message.decode("ascii").replace("BAN ", "")
                if username in NICKNAMES:
                    kick(username)
                    BANNED_USERS.append(username)
                else:
                    client.send("CMDERROR".encode("ascii"))
            else:
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

        # Checking if Nickname is Admin
        if nickname == "Admin":
            client.send("ADMINPASS".encode("ascii"))
            password = client.recv(1024).decode("ascii")

            # Check if password is equal to
            # the admin password.
            if password != "adminpass":
                # Closing Client Connection.
                client.send("REFUSED".encode("ascii"))
                client.close()
                continue

        NICKNAMES.append(nickname)
        CLIENTS.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode("ascii"))
        client.send("Connected to server!".encode("ascii"))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


# Kicking users.
# Accepts a user as a parameter
# and kicks the user.
def kick(user):
    if user in NICKNAMES:
        index = NICKNAMES.index(user)
        client = CLIENTS[index]

        CLIENTS.remove(client)
        NICKNAMES.remove(user)

        client.send("KICKED".encode("ascii"))
        client.close()
        broadcast("{} was kicked by an Admin!".format(user).encode("ascii"))


if __name__ == "__main__":
    print("Server is listening...")
    receive()
