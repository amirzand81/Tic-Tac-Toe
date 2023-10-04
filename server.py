import socket
import threading
import time


def checkOnlineUser(s):
    try:
        s.getpeername()

    except OSError:
        return False

    return True


def updateOnlineUsers():

    offlines = []

    for i in range(len(online_users)):
        if not checkOnlineUser(online_users[i][1]):
            offlines.append(i)

    offlines.reverse()

    for i in offlines:
        del online_users[i]


def recive(sock):

    while True:
        try:
            t = time.strftime("%H:%M:%S", time.localtime())
            recv_data = sock.recv(1024).decode()

            if recv_data != "":

                command = recv_data.split()
                userid = command[1]

                if (command[0] == "start"):

                    online_users.append((userid, sock))
                    print(f"{t} - Accepted connection from {sock.getpeername()}")

                elif (command[0] == "off"):

                    print(f"{t} - Closing connection to {sock.getpeername()}")
                    index = int()

                    for i in range(len(online_users)):
                        if (sock == online_users[i][1]):
                            index = i

                    del online_users[index]
                    sock.close()

                elif (command[0] == "list"):
                    updateOnlineUsers()

                    onlineLists = "online "

                    for item in online_users:
                        if sock != item[1]:
                            onlineLists += item[0] + " - " + \
                                str(item[1].getpeername()) + "+"

                    sock.send(onlineLists[0:-1].encode())
                    print(f"{t} - Scan online users by {sock.getpeername()}")

        except OSError:
            pass


online_users = []

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("", 40123))

serverSocket.listen(100)
t = time.strftime("%H:%M:%S", time.localtime())
print(f"{t} - Listening on {('', 40123)}")

while True:
    sock, addr = serverSocket.accept()
    threading.Thread(target=recive, args=(sock,)).start()
