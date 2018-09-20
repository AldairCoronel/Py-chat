import sys, socket, threading
from src.protocol import Protocol
from src.client import Client
from src.status import Status

class Server:
    clients = []
    rooms = []
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    aceptarClientes = False

    def __init__(self, PORT):
        self.server.bind(('0.0.0.0', PORT))
        self.server.listen(10000)
        self.clients = []
        self.rooms = []
        self.aceptarClientes = True


    def name_is_unique(self, name):
        unique = True
        for client in self.clients:
            unique = unique and (False if name == client.get_name() else True)
        return unique


    def change_client_name(self, name, client):
        if self.name_is_unique(name):
            client.set_name(name)
            client.get_socket().send(bytes('Usuario actualizado exitosamente',
                                            'UTF-8'))
        else:
            client.get_socket().send(bytes('Nombre repetido', 'UTF-8'))


    def send_clients(self):
        listClients = ''
        for client in self.clients:
            listClients += str(client) + ', '
        for client in self.clients:
            client.get_socket().send(bytes(listClients, 'UTF-8'))

    def verify_user_existance(self, user):
        for client in self.clients:
            if user == client.get_name():
                return True
        return False


    def get_user_socket(self, user):
        for client in self.clients:
            if user == client.get_name():
                return client.get_socket()


    def send_public_message(self, userMessage):
        for client in self.clients:
            client.get_socket().send(bytes(userMessage, 'UTF-8'))


    def send_direct_message(self, user, message, client):
        if self.verify_user_existance(user):
            destination = self.get_user_socket(user)
            destination.send(bytes(message, 'UTF-8'))
        else:
            client.get_socket().send(bytes('Usuario no encontrado', 'UTF-8'))

    def verify_status(self, status, client):
        verified = True
        if status == client.get_status():
            client.get_socket().send(bytes('Estado enviado es igual a \
                                            tu estado actual','UTF-8'))
            verified = False
        elif status != Status.ACTIVE.value and \
             status != Status.AWAY.value and \
             status != Status.BUSY.value:
            client.get_socket().send(bytes('Manda un estado valido: \
                                            ACTIVE, AWAY o BUSY' ,'UTF-8'))
            verified = False
        return verified


    def change_user_status(self, status, client):
        if self.verify_status(status, client):
            client.set_status(status)
            client.get_socket().send(bytes('Estado actualizado exitosamente',
                                            'UTF-8'))

    def get_user_message(self, message, indice):
        userMessage = ''
        for i in range(indice, len(message)):
            userMessage += message[i] + ' '
        return userMessage


    def create_room(self, room_name, client):


    def receive_message(self, client):
        while True:
            message = client.get_socket().recv(1024)
            message = message.decode('utf-8')
            message = message.split(' ')

            if message[0] == Protocol.IDENTIFY.value and len(message) > 1:
                self.change_client_name(message[1], client)

            elif message[0] == Protocol.STATUS.value and len(message) > 1:
                self.change_user_status(message[1], client)

            elif message[0] == Protocol.MESSAGE.value and len(message) > 2:
                message_to_user = message[1]
                userMessage = self.get_user_message(message, 2)
                self.send_direct_message(message_to_user, userMessage, client)

            elif message[0] == Protocol.USERS.value:
                self.send_clients()

            elif message[0] == Protocol.PUBLICMESSAGE.value and len(message) > 1:
                userMessage = self.get_user_message(message, 1)
                self.send_public_message(userMessage)

            elif message[0] == Protocol.CREATEROOM.value and len(message) > 1:
                room_name = message[1]
                self.create_room(room_name, client)

            # elif message[0] == Protocol.INVITE.value:
            #
            # elif message[0] == Protocol.JOINROOM.value:
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
