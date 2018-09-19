import sys, socket, threading

class Server:
    clients = []
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    aceptarClientes = False
    def __init__(self, HOST, PORT):
        self.server.bind((HOST, PORT))
        self.server.listen(10000)
        self.clients = []
        self.aceptarClientes = True

    def recieve_message(self, connection, address, clients):
        while True:
            message = connection.recv(1024)
            message = message.decode("utf-8")
            args = []
            message = message.split(" ")
            if message[0] == "USERS":
                listClients = ""
                for client in self.clients:
                    listClients += str(client)
                for client in self.clients:
                    client.send(bytes(listClients, "UTF-8"))
            elif message[0] == "PUBLICMESSAGE":
                variable = ""
                for i in range(1, len(message)):
                    variable += message[i] + " "
                for client in self.clients:
                    client.send(bytes(variable, "UTF-8"))
            if not message:
                break

        # while True:
        #     message = connection.recv(1024)
        #     protocolo = message.decode("utf-8")
        #     if protocolo == "USERS":
        #         listClients = ""
        #         for client in self.clients:
        #             listClients += str(client)
        #         for client in self.clients:
        #             client.send(bytes(listClients, "UTF-8"))
        #     if not message:
        #         break

    def arriba(self):
        while self.aceptarClientes:
                connection, address = self.server.accept()
                # name = connection.server.recv(1024)
                print("acaba de conectarse")
                self.clients.append(connection)
                serverThread = threading.Thread(target = self.recieve_message,
                                args=(connection, address, self.clients))
                # serverThread.daemon = True
                serverThread.start()
                print(self.clients)


#
if len(sys.argv) != 3:
    print ("Error: necesitas pasar: archivo, IP, puerto.")
    exit()
if(str(sys.argv[1] == 'localhost')):
    HOST = '127.0.0.1'
else:
    HOST = str(sys.argv[1])
PORT = int(sys.argv[2])
server = Server(HOST, PORT)
server.arriba()
