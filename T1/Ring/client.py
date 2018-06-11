from node import Node
import sys
import socket
from threading import Thread
HOST = "192.168.1.2"
import time

class Client(Node):
	def __init__(self,  is_start, port):
		Node.__init__(self)
		self.port = port
		self.communicator_socket = None
		self.is_start = is_start

		self.next_port = None
		self.next_ip   = None
	def connect_server(self):
		self.connect(HOST, 10001)
		self.mysend(b"enter_ring " + str.encode(str(self.port)))
		thread = Thread(target=self.listen_ring)
		thread.start()

	def listen_ring(self):
		self.communicator_socket = socket.socket(
			socket.AF_INET, socket.SOCK_STREAM)
		self.communicator_socket.bind((HOST, self.port))
		print("listening on port " + str(self.port))
		self.communicator_socket.listen(5)
		temp = None
		while True:
			con, client = self.communicator_socket.accept()
            #print('conectado por ', client)
			while True:
				msg = con.recv(1024)
				if not msg: break
                #print (client, msg)
				smsg = msg.decode("utf-8")
				temp = smsg.split(" ")
				print(temp)
				if temp[0] == "start":
					print("entrei aqui")
					self.next_ip = temp[1]
					self.next_port = int(temp[2])
					if self.is_start:
						socket_temp = socket.socket(
							socket.AF_INET, socket.SOCK_STREAM)
						socket_temp.connect((self.next_ip, self.next_port))
						print("token está comigo, ele será passado para o próximo nodo" + str((self.next_ip, self.next_port))+" em 2 segundos")
						time.sleep(2)
						self.send_by_socket(socket_temp, b"hey nodo")
				else:
					socket_temp = socket.socket(
						socket.AF_INET, socket.SOCK_STREAM)
					socket_temp.connect((self.next_ip, self.next_port))
					print("token está comigo, ele será passado para o próximo nodo" + str((self.next_ip, self.next_port))+" em 2 segundos")
					time.sleep(2)
					self.send_by_socket(socket_temp, b"hey nodo")
				print(smsg)
			con.close()