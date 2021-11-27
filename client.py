import socket


HEADER = 64
PORT = 8000
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
SERVER = socket.gethostname()
# SERVER = "SERVER HOST IP"
ADDR = (SERVER, PORT)

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


if __name__ == "__main__":
    msg = input("Message: ")

    if len(msg) < 7:
        msg += ' ' * (7 - len(msg))
    send(msg)
    send(DISCONNECT_MSG)
