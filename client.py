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
        message = "{}: {}".format(NICKNAME, input(""))
        CLIENT.send(message.encode("ascii"))


# Starting Threads For Recieving And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
