import socket

class Node:
    """demonstration class only
      - coded for clarity, not efficiency
    """

    def __init__(self, _socket=None):
        if _socket is None:
            self.socket = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.socket = _socket

    def connect(self, host, port):
        self.socket.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        MSGLEN = len(msg)
        while totalsent < MSGLEN:
            sent = self.socket.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socketet connection broken")
            totalsent = totalsent + sent
    def send_by_socket(self, socket, msg):
        totalsent = 0
        MSGLEN = len(msg)
        while totalsent < MSGLEN:
            sent = socket.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socketet connection broken")
            totalsent = totalsent + sent
    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.socket.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socketet connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)