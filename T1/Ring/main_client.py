from client import Client
import sys
import time
from threading import Thread

if __name__ == "__main__":
	is_start = False
	print((sys.argv[3]))
	if sys.argv[3] == 's':
		is_start = True
		print(is_start)
	client = Client(is_start, int(sys.argv[2]))
	client.listen_ring()