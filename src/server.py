import sys, socket, threading
from src.protocol import Protocol

class Server:
    clients = []
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    aceptarClientes = False
    def __init__(self, PORT):
        self.server.bind(('0.0.0.0', PORT))
        self.server.listen(10000)
        self.clients = []
        self.aceptarClientes = True

    def verify_name(name, clients):
        if (name < 2 || name > 15)
            print('El nombre debe tener entre 2 y 15 caracteres')
        elif
            for client in clients:   



    def get_name(clients, connection):
            if (connection.lenght != 0):
                name = connection
                verify_name(name, clients)
            else:
                print('Necesitas mandarme un nombre de usuario.')
                break

    def change_client_name(connection, address, clients):
        name = get_name(clients, connection)

    def recieve_message(self, connection, address, clients):
        while True:
            message = connection.recv(1024)
            message = message.decode('utf-8')
            args = []
            message = message.split(' ')
            if message[0] == Protocol.IDENTIFY.value:
                change_client_name(message[1], address, clients)

            # elif message[0] == Protocol.STATUS.value:
            #
            #
            # elif message[0] == Protocol.MESSAGE.value:


            elif message[0] == Protocol.USERS.value:
                listClients = ''
                for client in self.clients:
                    listClients += str(client)
                for client in self.clients:
                    client.send(bytes(listClients, 'UTF-8'))

            elif message[0] == Protocol.PUBLICMESSAGE.value:
                variable = ''
                for i in range(1, len(message)):
                    variable += message[i] + ' '
                for client in self.clients:
                    client.send(bytes(variable, 'UTF-8'))

            # elif message[0] == Protocol.CREATEROOM.value:
            #
            #
            # elif message[0] == Protocol.INVITE.value:
            #
            #
            # elif message[0] == Protocol.JOINROOM.value:
            #
            #
            # elif message[0] == Protocol.ROOMMESSAGE.value:



            if not message:
                break

    def arriba(self):
        while self.aceptarClientes:
                connection, address = self.server.accept()
                # name = connection.server.recv(1024)
                print('acaba de conectarse')
                self.clients.append(connection)
                serverThread = threading.Thread(target = self.recieve_message,
                                args=(connection, address, self.clients))
                # serverThread.daemon = True
                serverThread.start()
                print(self.clients)
