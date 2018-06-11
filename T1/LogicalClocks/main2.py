from server import Lamport
from threading import Thread

if __name__ == "__main__":
	node = Lamport()
	node.connect('192.168.1.5', 10000)
	node.mysend(b"ola")