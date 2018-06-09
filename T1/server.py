import socket
import sys


DEFAULT_ADDRESS = 'localhost'

class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 10000
        self.server_address = (DEFAULT_ADDRESS, self.port)

    def bind(self):
        self.socket.bind(self.server_address)
    def listen_for_connections(self):
        self.socket.listen(1)
        while(True):

            print('esperando conexão')
            connection, client_address = self.socket.accept()
            try:
                print('cliente conectado ', self.socket.accept())
                while True:
                    data = connection.recv(16)
                    print('received{!r}'.format(data))
                    if data:
                        print('sending data back to the client')
                        connection.sendall(data)
                    else:
                        print('no data from ', client_address)
                        break
            finally:
                connection.close()