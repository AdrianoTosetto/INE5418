from client import Client
import sys

if __name__ == "__main__":

	client = Client()
	client.connect('localhost', 10000)

	client.mysend(b"req_resource " + str.encode(sys.argv[1] + " " + sys.argv[2]))