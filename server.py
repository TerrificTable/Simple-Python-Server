import threading
import socket

HEADER = 64
PORT = 8000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr[0]}:{addr[1]}")

    connected = True
    try:
        while connected:
            msgLength = conn.recv(HEADER).decode(FORMAT)
            if msgLength:
                msgLength = int(msgLength)
                msg = conn.recv(msgLength).decode(FORMAT)

                if not msg == DISCONNECT_MSG:
                    print(f"[{addr[0]}] {msg}")
                    conn.send("Received".encode(FORMAT))
                else:
                    connected = False
        conn.close()
    except ConnectionResetError:
        print(f"[{addr[0]}] Client closed connection")


def start():
    server.listen()
    print("[STARTED] Server is listening on {}:{}".format(SERVER, PORT))
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr,))
        thread.start()
        print(
            f"\r[ACTIVE CONNECTIONS] {threading.active_count() -1}", end="\r")


if __name__ == "__main__":
    print("[STARTING] Server is starting")
    start()
