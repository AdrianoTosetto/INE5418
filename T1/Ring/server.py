from node import Node
import sys
import time
from threading import Thread
import queue
import socket

HOST = "192.168.1.2"

class Server(Node):
    using_resource = False
    NODES_RING = 0
    def __init__(self):
        Node.__init__(self)
        self.ring_nodes = []

    def listen(self):
        self.ring_nodes.append(('192.168.1.2', 10003))
        self.ring_nodes.append(('192.168.1.2', 10005))
        i = 0
        _len = len(self.ring_nodes)
        for i in range(_len):
            ssocket = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
            ssocket.connect((self.ring_nodes[i][0], int(self.ring_nodes[i][1])))
            totalsent = 0
            msg = str.encode("start "+ self.ring_nodes[(i+1) % _len][0] + " " + str(self.ring_nodes[(i+1) % _len][1]))
            MSGLEN = len(msg)
            while totalsent < MSGLEN:
                sent = ssocket.send(msg[totalsent:])
                if sent == 0:
                    raise RuntimeError("socketet connection broken")
                totalsent = totalsent + sent


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
        fo.close()
        time.sleep(2)