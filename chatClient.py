import socket
import threading


tLock = threading.Lock()
shutdown = False


def receiving(sock):
    while not shutdown:
        try:
            tLock.acquire()
            while True:
                data = sock.recvfrom(1024)[0]
                data = data.decode()
                print(str(data))
        except (BlockingIOError, RuntimeError):
            pass
        finally:
            tLock.release()


host = "127.0.0.1"
port = 0

server = (host, 2001)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

rT = threading.Thread(target=receiving, kwargs={'sock': s})
rT.start()

alias = input("Name: ")
s.sendto(str("connect "+alias).encode(), server)
message = alias

while message != 'q':
    if message != '':
        message = input()
        s.sendto(str(message).encode(), server)

s.sendto(str('q').encode(), server)
shutdown = True
s.close()
rT.join()
