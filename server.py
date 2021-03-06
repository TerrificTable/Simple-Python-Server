'''
This Code was Written by TerrificTable55™#5297 (https://github.com/TerrificTable)
If you want to use this don't remove this or/and add me to credits
You can sell this code if you want just credit me
For everything else: https://raw.githubusercontent.com/TerrificTable/Simple-Python-Server/main/LICENSE  |  https://github.com/TerrificTable/Simple-Python-Server/blob/main/LICENSE

1:30AM | 12/1/2021
'''
from plyer import notification
from colorama import Fore
import threading
import socket

HEADER = 64  # the length of the message sending the length of the acutal message to the server
PORT = 8000  # the port
# server IP (uses your device IP as default)
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)  # the address consisting of IP and Port
FORMAT = 'utf-8'  # the format for de/encoding the messages
DISCONNECT_MSG = "!DISCONNECT"  # Server/Client key for disconnect
NOTIFICATION_MSG = "!NOTIFY"  # Server/Client key for notifications
ERROR_MSG = "!ERROR"  # Server/Client key for errors
EXEC_MSG = "!EXEC"  # Server/Client key to execute code

filler = f"press ENTER to not execute code"
errTitle = f" ran into an error"


r = Fore.RED
g = Fore.GREEN
c = Fore.CYAN
m = Fore.MAGENTA
y = Fore.YELLOW
w = Fore.WHITE


# setting up the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)  # binding the server to IP and Port


def notify(title, message, icon=None):  # the notification system uses plyer
    notification.notify(title=title, message=message,
                        app_icon=icon, timeout=10)


class Server():  # the server it self
    def __init__(self, SERVER, PORT, FORMAT):
        self.SERVER = SERVER
        self.PORT = PORT
        self.FORMAT = FORMAT

    def handle_client(self, conn, addr):  # client handler
        # prints out if a new client connects to the server
        print(f"{w}[{g}NEW CONNECTION{w}] {addr[0]}:{addr[1]}")

        connected = True
        try:
            while connected:
                # takes the from the client sent message length
                msgLength = conn.recv(HEADER).decode(self.FORMAT)

                if msgLength:
                    msgLength = int(msgLength)
                    # waits for a message with the from client sent msg length
                    msg = conn.recv(msgLength).decode(self.FORMAT)
                    omsg = msg

                    if not msg == DISCONNECT_MSG:  # if the client doesn't disconnects
                        # if the message starts with the notification key
                        if str(msg).startswith(NOTIFICATION_MSG):
                            msg = str(msg).replace(NOTIFICATION_MSG, "")
                            # sends a windows notification with the msg from the client sent
                            notify("["+str(addr[0])+"] sent Notification", msg)

                        elif str(msg).startswith(ERROR_MSG):
                            msg = str(msg).replace(ERROR_MSG, "")
                            # sends a windows notification with the error/msg the client sent
                            notify("["+str(addr[0])+"] ran into an ERROR", msg)
                            msg = f"{w}[{r}ERROR{w}]: " + msg

                        elif str(msg).startswith(EXEC_MSG):
                            omsg = msg
                            msg = str(msg).replace(EXEC_MSG, "")
                            notify(
                                f"[{str(addr[0])}] Allows you to execute Code", filler)
                            # code input
                            if msg.__contains__("custom"):
                                code = input(f"{w}[{y}{addr[0]}{w}] Code to Execute: ").encode(
                                    self.FORMAT)
                                msg = "Code Executed"
                                if code.decode(self.FORMAT) == "":
                                    code = "print('No Code was Executed')".encode(
                                        self.FORMAT)
                                    msg = ""

                            # Execute code
                            conn.send(EXEC_MSG.encode(self.FORMAT) + code)

                        # Prints out the msg the client sent
                        if not str(omsg).startswith(EXEC_MSG):
                            conn.send(f'Receved'.encode(self.FORMAT))
                        print(f"{w}[{m}{addr[0]}{w}]{c} {msg}")
                        # sends a confirmation that the server receved the message

                    else:
                        connected = False
            conn.close()
            # if the client disconnects
            print(f"{w}[{r}{addr[0]}{w}] Connection closed")
        except ConnectionResetError:
            # if the client disconnects
            print(f"{w}[{r}{addr[0]}{w}] Client closed connection")

    def start(self):  # starts the server itself
        server.listen()  # starts listening for stuff
        print(
            f"{w}[{g}STARTED{w}] Server is listening on {self.SERVER}:{self.PORT}")  # just for debug

        while True:
            # accepts client connection to the server (i think you can set a whitelist for that but not sure)
            conn, addr = server.accept()
            thread = threading.Thread(
                target=self.handle_client, args=(conn, addr,))  # creates a new thread for every client
            thread.start()  # starts the thread
            print(
                f"\r{w}[ACTIVE CONNECTIONS{w}] {threading.active_count() -1}", end="\r")  # prints the current active connections


if __name__ == "__main__":
    print(f"{w}[{y}STARTING{w}] Server is starting")
    Server(SERVER, PORT, FORMAT).start()  # starting the server
