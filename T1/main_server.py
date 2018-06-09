from server import Server

if __name__ == "__main__":

	server = Server()
	server.bind()
	server.listen_for_connections()