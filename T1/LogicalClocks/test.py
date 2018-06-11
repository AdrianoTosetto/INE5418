#!/usr/bin/env python
#
# Send/receive UDP multicast packets.
# Requires that your OS kernel supports IP multicast.
#
# Usage:
#   mcast -s (sender, IPv4)
#   mcast -s -6 (sender, IPv6)
#   mcast    (receivers, IPv4)
#   mcast  -6  (receivers, IPv6)

MYPORT = 8123
MYGROUP_4 = '225.0.0.250'
MYGROUP_6 = 'ff15:7079:7468:6f6e:6465:6d6f:6d63:6173'
MYTTL = 1 # Increase to reach other networks

import time
import struct
import socket
import sys
from threading import Thread
import queue

def main():
    group = MYGROUP_6 if "-6" in sys.argv[1:] else MYGROUP_4

    if "-s" in sys.argv[1:]:
        sender(group)
    else:
        receiver(group)


def sender(group=MYGROUP_4):
    addrinfo = socket.getaddrinfo(group, None)[0]

    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

    # Set Time-to-live (optional)
    ttl_bin = struct.pack('@i', MYTTL)
    if addrinfo[0] == socket.AF_INET: # IPv4
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)
    else:
        s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl_bin)

   
    while True:
        data = input("digite algo\n")
        if data == "s":
            send = str(time.time())
        s.sendto(str.encode(send + '\0'), (addrinfo[4][0], MYPORT))
        time.sleep(1)


def receiver(group=MYGROUP_4):
    # Look up multicast group address in name server and find out IP version
    addrinfo = socket.getaddrinfo(group, None)[0]

    # Create a socket
    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

    # Allow multiple copies of this program on one machine
    # (not strictly needed)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind it to the port
    s.bind(('', MYPORT))

    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
    # Join group
    if addrinfo[0] == socket.AF_INET: # IPv4
        mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    else:
        mreq = group_bin + struct.pack('@I', 0)
        s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

    # Loop, printing any data we receive
    print('waiting')
    while True:
        data, sender = s.recvfrom(1500)
        while data[-1:] == '\0': data = data[:-1] # Strip trailing \0's
        print (str(sender) + '  ' + repr(data))


class Lamport():
    OK = 0
    WANTED = 1
    HELD = 2
    def __init__(self):
        print("starting")
        self.state = Lamport.OK
        #self.requests = Queue.queue()


    def start(self):
        thread1 = Thread(target = self.listen(), args = (group))
        thread2 = Thread(target = self.sender(), args = (group))
        thread1.start()
        thread2.start()
    def sender(self, group=MYGROUP_4):
        addrinfo = socket.getaddrinfo(MYGROUP_4, None)[0]

        s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

        # Set Time-to-live (optional)
        ttl_bin = struct.pack('@i', MYTTL)
        if addrinfo[0] == socket.AF_INET: # IPv4
            s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)
        else:
            s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl_bin)

        while True:
            data = input("digite algo\n")
            if data == "s":
                send = str(time.time())
            s.sendto(str.encode(send + '\0'), (addrinfo[4][0], MYPORT))
            time.sleep(1)
            ssocket = socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM)
            ssocket.bind(('192.168.1.6', 10000))
            ssocket.listen(5)
            while True:
                con, client = ssocket.accept()
                print('conectado por ', client)
                while True:
                    msg = con.recv(1024)
                    if not msg: 
                        break
                        smsg = msg.decode("utf-8")
                        print(smsg)
            con.close()
    def mysend(self, client, msg):
        totalsent = 0
        MSGLEN = len(msg)
        while totalsent < MSGLEN:
            sent = client.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socketet connection broken")
            totalsent = totalsent + sent


    def listen(self, group=MYGROUP_4):
        # Look up multicast group address in name server and find out IP version
        addrinfo = socket.getaddrinfo(MYGROUP_4, None)[0]

        # Create a socket
        s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

        # Allow multiple copies of this program on one machine
        # (not strictly needed)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind it to the port
        s.bind(('', MYPORT))

        group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
        # Join group
        if addrinfo[0] == socket.AF_INET: # IPv4
            mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        else:
            mreq = group_bin + struct.pack('@I', 0)
            s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

        # Loop, printing any data we receive
        print('waiting')
        while True:
            data, sender = s.recvfrom(1500)
            while data[-1:] == '\0': data = data[:-1] # Strip trailing \0's
            socketr = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
            print(data)
            socketr.connect(('192.168.1.6', 10000))
            totalsent = 0
            msg = "Ok"
            MSGLEN = len(msg)
            while totalsent < MSGLEN:
                sent = self.socket.send(msg[totalsent:])
                if sent == 0:
                    raise RuntimeError("socketet connection broken")
                totalsent = totalsent + sent


if __name__ == '__main__':
    group = MYGROUP_6 if "-6" in sys.argv[1:] else MYGROUP_4
    l = Lamport()
    thread1 = Thread(target = l.listen)
    thread1.start()
    thread2 = Thread(target = l.sender)
    thread2.start()

    thread1.join()
    thread2.join()
    print("thread2")
