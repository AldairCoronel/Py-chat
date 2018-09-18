import sys, socket
from tread import *

class Server:
    clients = []
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __init__(self, HOST, PORT):
        self.server.bind((HOST, PORT))
        self.server.listen(10000)
        self.clients = []

#    def handler(self, connection, address):


    def accept_new_client(self):
        while True:
                connection, address = self.server.accept()
                name = connection.server.recv(1024)
                print("%s acaba de conectarse" %name)
                self.clients.append(connection)
                clientThread = threading.Thread(target = self.handler, args=(Co, PORT))
                clientThread.daemon = True
                clientThread.start()
                print(self. clients)



if len(sys.argv) != 3
    print "Error: necesitas pasar: archivo, IP, puerto."
    exit()
HOST = str(sys.argv[1])
PORT = str(sys.argv[2])
server = Server(HOST, PORT)
server.run
