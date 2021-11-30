import os
import socket


HEADER = 64
PORT = 8000
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
NOTIFICATION_MSG = "!NOTIFY"
ERROR_MSG = "!ERROR"
SERVER = socket.gethostname()
# SERVER = "SERVER HOST IP"
ADDR = (SERVER, PORT)

msg = ""


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msgLength = len(message)
    sendLength = str(msgLength).encode(FORMAT)
    sendLength += b' ' * (HEADER - len(sendLength))

    client.send(sendLength)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


def test():
    try:
        os.system("cd C:/Users/Sandbox/A")
        return ""
    except Exception as e:
        return e


if __name__ == "__main__":
    msg = ""
    msg = input("Message: ")
    if msg.startswith("#notify"):
        msg = NOTIFICATION_MSG + msg.replace("#notify", "")
    if msg.startswith("#error"):
        msg = ERROR_MSG + msg.replace("#error", "")

    if len(msg) < 7:
        msg += ' ' * (7 - len(msg))

    send(msg)
    send(DISCONNECT_MSG)
