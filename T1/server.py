from node import Node
from socket import socket
import sys
import time
from threading import Thread
import queue

requests = queue.Queue()

class Server(Node):
    using_resource = False
    def __init__(self):
        Node.__init__(self)

    def listen(self):
        self.socket.bind(('localhost', 10000))
        self.socket.listen(5)

        while True:
            con, client = self.socket.accept()
            #print('conectado por ', client)
            while True:
                msg = con.recv(1024)
                if not msg: break
                print (client, msg)
                smsg = msg.decode("utf-8")
                command = smsg.split(" ")
                print(command)
                if command[0] == "req_resource":
                    thread = Thread(target = handle_req, args = ('localhost', command[1], command[2] ))
                    thread.start()

            #print ('Finalizando conexao do cliente', client)
            con.close()



def handle_req(ip,file, content):
    if not Server.using_resource:
        if requests.empty():
            fo = open(file, "a+")
            fo.write(content)
            Server.using_resource = True
            time.sleep(10)
            Server.using_resource = False
            thread = Thread(target = handle_queue_requests)
            thread.start()
        else:
            requests.put((ip, file, content))
            print('waiting')

    else:
        requests.put((ip, file, content))

def handle_queue_requests():
    while not requests.empty():
        client = requests.get()
        print("handling " + client[0])

        fo = open(client[1], "a+")
        fo.write(client[2])
        time.sleep(2)