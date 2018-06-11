from test import Lamport
from threading import Thread

if __name__ == "__main__":
	node = Lamport()
	thread = Thread(target = node.listen())
	thread.start()