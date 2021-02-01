import getpass
import socket
import threading

# Connection Data
HOST = "127.0.0.1"
PORT = 55555

# Choosing Nickname
NICKNAME = input("Choose your nickname: ")

# Check if Nickname is Admin
if NICKNAME == "Admin":
    PASSWORD = getpass.getpass("Enter Password for Admin: ")

# Connecting To Server
CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT.connect((HOST, PORT))

# Commands
ADMIN_COMMANDS = {
    "/ban": "To ban a Client. Usage: /ban {Nickname}",
    "/clients": "To see a list of Connected Clients. Usage: /clients",
    "/commands": "To see the list of Commands. Usage: /commands",
    "/kick": "To kick a Client. Usage: /kick {Nickname}",
}

CLIENT_COMMANDS = {
    "!commands": "To see the list of Commands. Usage: !commands",
    "!quit": "To quit from the chat. Usage: !quit",
}

# Set RUNNING to True
RUNNING = True


# Listening to Server and Sending Nickname,
# Listens for message and if message == "NICK",
# send Nickname to Server. Close the connection
# if a connection error occurs.
def receive():
    while RUNNING:
        try:
            # Receiving Message From Server
            message = CLIENT.recv(1024).decode("ascii")
            if message == "NICK":
                CLIENT.send(NICKNAME.encode("ascii"))
            elif message == "ADMINPASS":
                CLIENT.send(PASSWORD.encode("ascii"))
            elif message == "REFUSED":
                print("Connection was refused. Wrong Password!")
                exit()
            elif message == "KICKED":
                print("You were kicked by an Admin")
                exit()
            elif message == "BAN":
                print("Connection refused due to ban.")
                exit()
            elif message == "CMDERROR":
                print("Invalid Command")
            elif message.startswith("CLIENTS"):
                clients_list = message.split()[1:]
                for index, client in enumerate(clients_list):
                    print(index + 1, client)
            else:
                print(message)
        except Exception as err:
            raise err
            # Close Connection When Error
            print("An error occured!")
            CLIENT.close()
            exit()


# Sending Messages To Server
# Wait for user input and
# send the message.
def write():
    global RUNNING

    while True:
        message = input()

        # Check for commands
        if message.startswith("/"):
            if NICKNAME == "Admin":
                if message.startswith("/kick"):
                    username = message.replace("/kick ", "")
                    CLIENT.send("KICK {}".format(username).encode("ascii"))
                elif message.startswith("/ban"):
                    username = message.replace("/ban ", "")
                    CLIENT.send("BAN {}".format(username).encode("ascii"))
                elif message.startswith("/commands"):
                    for key, value in ADMIN_COMMANDS.items():
                        print("{}: {}".format(key, value))
                elif message.startswith("/clients"):
                    CLIENT.send("CLIENTSLIST".encode("ascii"))
                else:
                    print("Invalid Command")
            else:
                print("Commands can only be executed by an Admin")
        elif message.startswith("!"):
            if message.startswith("!quit"):
                if input("Do You want to quit? ").lower().startswith("y"):
                    RUNNING = False
            elif message.startswith("!commands"):
                for key, value in CLIENT_COMMANDS.items():
                    print("{}: {}".format(key, value))
            else:
                print("Invalid Command")
        else:
            message = "{}: {}".format(NICKNAME, message)
            CLIENT.send(message.encode("ascii"))


# Starting Threads For Recieving And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write, daemon=True)
write_thread.start()
