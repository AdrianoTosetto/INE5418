from node import Node
from socket import socket
import sys
import time
from threading import Thread
import queue

requests = queue.Queue()

class Lamport(Node):
    using_resource = False
    def __init__(self):
        Node.__init__(self)

    def listen(self):
        self.socket.bind(('192.168.1.5', 10000))
        self.socket.listen(5)

        while True:
            con, client = self.socket.accept()
            print('conectado por ', client)
            while True:
                msg = con.recv(1024)
                if not msg: break
                #print (client, msg)
                smsg = msg.decode("utf-8")
                command = smsg.split(" ")
                print(command)
                if command[0] == "req_resource":
                    thread = Thread(target = handle_req, args = ('localhost', command[1], command[2] ))
                    thread.start()

            #print ('Finalizando conexao do cliente', client)
            con.close()