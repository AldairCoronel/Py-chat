import sys, socket, threading
from src.protocol import Protocol
from src.client import Client

class Server:
    clients = []
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    aceptarClientes = False
    def __init__(self, PORT):
        self.server.bind(('0.0.0.0', PORT))
        self.server.listen(10000)
        self.clients = []
        self.aceptarClientes = True

    def name_is_unique(self, name):
        unique = True
        for client in self.clients:
            unique = unique and (False if name == client.get_name() else True)
        return unique

    def change_client_name(self, name, client):
        if self.name_is_unique(name):
            client.set_name(name)
        else:
            client.get_socket().send(bytes('Nombre repetido', 'UTF-8'))



    def send_clients(self):
        listClients = ''
        for client in self.clients:
            listClients += str(client)
        for client in self.clients:
            client.get_socket().send(bytes(listClients, 'UTF-8'))

    def send_message(self, userMessage):
        for client in self.clients:
            client.get_socket().send(bytes(userMessage, 'UTF-8'))


    def receive_message(self, client):
        while True:
            message = client.get_socket().recv(1024)
            message = message.decode('utf-8')
            message = message.split(' ')
            if message[0] == Protocol.IDENTIFY.value and len(message) > 1:
                self.change_client_name(message[1], client)

            # elif message[0] == Protocol.STATUS.value:
            #
            #
            # elif message[0] == Protocol.MESSAGE.value:


            elif message[0] == Protocol.USERS.value:
                self.send_clients()

            elif message[0] == Protocol.PUBLICMESSAGE.value:
                userMessage = ''
                for i in range(1, len(message)):
                    userMessage += message[i] + ' '
                self.send_message(userMessage)

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
                client = Client(None, connection, address)
                print('Acaba de conectarse ', address)
                self.clients.append(client)
                serverThread = threading.Thread(target = self.receive_message,
                                args=(client,))
                # serverThread.daemon = True
                serverThread.start()
