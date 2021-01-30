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


# Listening to Server and Sending Nickname,
# Listens for message and if message == "NICK",
# send Nickname to Server. Close the connection
# if a connection error occurs.
def receive():
    while True:
        try:
            # Receive Message From Server
            # If "NICK" Send Nickname
            message = CLIENT.recv(1024).decode("ascii")
            if message == "NICK":
                CLIENT.send(NICKNAME.encode("ascii"))
            elif message == "ADMINPASS":
                CLIENT.send(PASSWORD.encode("ascii"))
            elif message == "REFUSED":
                print("Connection was refused. Wrong Password!")
                quit()
            elif message == "CMDERROR":
                print("Invalid Command")
            elif message == "KICKED":
                print("You were kicked by an Admin")
                quit()
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            CLIENT.close()
            break


# Sending Messages To Server
# Wait for user input and
# send the message.
def write():
    while True:
        message = input("")

        # Check for commands
        if message.startswith("/"):
            if NICKNAME == "Admin":
                if message.startswith("/kick "):
                    username = message.replace("/kick ", "")
                    CLIENT.send("KICK {}".format(username).encode("ascii"))
                elif message.startswith("/ban "):
                    username = message.replace("/ban ", "")
                    CLIENT.send("BAN {}".format(username).encode("ascii"))
                else:
                    print("Invalid Command")
            else:
                print("Commands can only be executed by an Admin")
        else:
            message = "{}: {}".format(NICKNAME, message)
            CLIENT.send(message.encode("ascii"))


# Starting Threads For Recieving And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
