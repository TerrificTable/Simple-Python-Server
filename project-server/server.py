import os
from plyer import notification
from colorama import Fore
import threading
import socket

HEADER = 64
PORT = 8000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
NOTIFICATION_MSG = "!NOTIFY"
ERRORO_MSG = "!ERROR"

errTitle = f" ran into an error"
# icon = f"{os.getcwd()}icon.ico"


r = Fore.RED
g = Fore.GREEN
c = Fore.CYAN
m = Fore.MAGENTA
y = Fore.YELLOW
w = Fore.WHITE


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def notify(title, message, icon=None):
    notification.notify(title=title, message=message,
                        app_icon=icon, timeout=10)


class Server():
    def __init__(self, SERVER, PORT, FORMAT):
        self.SERVER = SERVER
        self.PORT = PORT
        self.FORMAT = FORMAT

    def handle_client(self, conn, addr):
        print(f"{w}[{g}NEW CONNECTION{w}] {addr[0]}:{addr[1]}")

        connected = True
        try:
            while connected:
                msgLength = conn.recv(HEADER).decode(self.FORMAT)
                if msgLength:
                    msgLength = int(msgLength)
                    msg = conn.recv(msgLength).decode(self.FORMAT)

                    if not msg == DISCONNECT_MSG:
                        if str(msg).startswith(NOTIFICATION_MSG):
                            notific = str(msg).replace(NOTIFICATION_MSG, "")
                            notify(str(addr[0])+" NOTIFICATION SENT", notific)

                        print(f"{w}[{m}{addr[0]}{w}]{c} {msg}")
                        conn.send("Received".encode(self.FORMAT))
                    else:
                        connected = False
            conn.close()
            print(f"{w}[{r}{addr[0]}{w}] Connection closed")
        except ConnectionResetError:
            print(f"{w}[{r}{addr[0]}{w}] Client closed connection")

    def start(self):
        server.listen()
        print(
            f"{w}[{g}STARTED{w}] Server is listening on {self.SERVER}:{self.PORT}")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(
                target=self.handle_client, args=(conn, addr,))
            thread.start()
            print(
                f"\r{w}[ACTIVE CONNECTIONS{w}] {threading.active_count() -1}", end="\r")


if __name__ == "__main__":
    print(f"{w}[{y}STARTING{w}] Server is starting")
    Server(SERVER, PORT, FORMAT).start()


# if str(msg).startswith("#py "):
#     code = msg.replace("#py ", "")
#     exec(code)
