"""
This Code was Written by TerrificTable55™#5297 (https://github.com/TerrificTable)
If you want to use this don't remove this or/and add me to credits
You can sell this code if you want just credit me
For everything else: https://raw.githubusercontent.com/TerrificTable/Simple-Python-Server/main/LICENSE  |  https://github.com/TerrificTable/Simple-Python-Server/blob/main/LICENSE

1:30AM | 12/1/2021
"""
import socket
import os


HEADER = 64  # Headder Length for sending the length of the actual message
PORT = 8000  # Port
FORMAT = 'utf-8'  # De/Encoding format
DISCONNECT_MSG = "!DISCONNECT"  # Client and Server key for disconnect
NOTIFICATION_MSG = "!NOTIFY"  # Client and Server key for notifications
ERROR_MSG = "!ERROR"  # Client and Server key for errors
# the host IP as a string (takes your private if if your using the line as it is)
SERVER = socket.gethostname()
# SERVER = "SERVER HOST IP"
# Server Address its the IP and the Port for socket to connect to
ADDR = (SERVER, PORT)

msg = ""


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Setting up client
client.connect(ADDR)  # Connect to server


def send(msg):
    message = msg.encode(FORMAT)  # encode message
    msgLength = len(message)
    sendLength = str(msgLength).encode(FORMAT)
    sendLength += b' ' * (HEADER - len(sendLength))

    client.send(sendLength)  # send length of actual msg to server
    client.send(message)  # sends the msg itself
    # Prints what the Client receves if the server awnsers (max of 2048 bytes/characters)
    print(client.recv(2048).decode(FORMAT))


def test():  # Just a test function
    try:
        os.system("cd C:/Users/usr/A")
        return ""
    except Exception as e:
        return e


if __name__ == "__main__":
    msg = input("Message: ")  # message it self

    if msg.startswith("#notify"):
        # removes "#notify" from msg if it starts with it
        msg = NOTIFICATION_MSG + msg.replace("#notify", "")
    if msg.startswith("#error"):
        # removes "#error" from msg if it starts with it
        msg = ERROR_MSG + msg.replace("#error", "")

    # for fixing bugs cuz if the length of the message is less than 6 i think it will just add the number of missing chars/bytes to fill minimum length
    if len(msg) < 7:
        msg += ' ' * (7 - len(msg))  # the fix itself

    send(msg)  # sends the msg to the server
    send(DISCONNECT_MSG)  # sends disconnect to server
