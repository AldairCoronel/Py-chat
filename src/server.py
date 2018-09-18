import sys, socket
from tread import *

class Server:
    clients = []
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __init__(self, HOST, PORT):
        self.server.bind((HOST, PORT))
        self.server.listen(10000)
        self.clients = []



if len(sys.argv) != 3
    print "Error: necesitas pasar: archivo, IP, puerto."
    exit()
HOST = str(sys.argv[1])
PORT = str(sys.argv[2])
server = Server(HOST, PORT)
server.run
