from node import Node
from socket import socket
import sys
import time
from threading import Thread
import queue

requests = list()

def str_queue():
    print("size = " + str(requests.qsize()))
    for e in iter(requests.get, None):
        print("client = " + str(e[0]), end=" ")
        print("porta = " + str(e[1]))

def str_queue1():
    print("size = " + str(len(requests)))
    for e in requests:
        print("client = " + str(e[0]), end=" ")
        print("porta = " + str(e[1]))


class Server(Node):
    using_resource = False
    def __init__(self):
        Node.__init__(self)

    def listen(self):
        self.socket.bind(('192.168.1.3', 10000))
        self.socket.listen(5)

        while True:
            con, client = self.socket.accept()
            #print('conectado por ', client)
            while True:
                msg = con.recv(1024)
                if not msg: break
                #print (client, msg)
                smsg = msg.decode("utf-8")
                command = smsg.split(" ")
                if command[0] == "req_resource":
                    thread = Thread(target = handle_req, args = (client[0], client[1], command[1], command[2] ))
                    thread.start()

            #print ('Finalizando conexao do cliente', client)
            con.close()



def handle_req(ip,port, file, content):
    if not Server.using_resource:
        if len(requests) == 0:
            fo = open(file, "a+")
            fo.write(content)
            Server.using_resource = True
            time.sleep(10)
            Server.using_resource = False
            thread = Thread(target = handle_queue_requests)
            thread.start()
        else:
            requests.append((ip, port, file, content))
            print('waiting')

    else:
        requests.append((ip, port, file, content))
        print("Alguém já está usando o recurso")

    str_queue1()

def handle_queue_requests():
    print("starting handling")
    while len(requests) > 0:
        client = requests.pop(0)
        print("Tirando da fila o nodo: " + client[0] + " pela porta " + client[1])

        fo = open(client[2], "a+")
        fo.write(client[3])
        fo.close()
        time.sleep(2)
    Server.using_resource = False