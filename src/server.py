import sys, socket, threading
from src.protocol import Protocol
from src.client import Client
from src.status import Status
from src.room import Room

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
            client.get_socket().send(bytes('Estado enviado es igual a'
                                           'tu estado actual','UTF-8'))
            verified = False
        elif status != Status.ACTIVE.value and \
             status != Status.AWAY.value and \
             status != Status.BUSY.value:
            client.get_socket().send(bytes('Manda un estado valido: '
                                           'ACTIVE, AWAY o BUSY' ,'UTF-8'))
            verified = False
        return verified


    def change_user_status(self, status, client):
        if self.verify_status(status, client):
            client.set_status(status)
            client.get_socket().send(bytes('Estado actualizado exitosamente',
                                            'UTF-8'))


    def get_user_message(self, message, index):
        userMessage = ''
        for i in range(index, len(message)):
            userMessage += message[i] + ' '
        return userMessage


    def get_sockets(self, users):
        sockets = []
        for user in users:
            for client in self.clients:
                if user == client.get_name():
                    sockets.append(client.get_socket())
        return sockets


    def verify_chat_room_duplicate(self, roomName):
        for room in self.rooms:
            if roomName == room.get_name():
                return False
        return True

    def verify_chat_room_existance(self, roomName):
        for room in self.rooms:
            if roomName == rom.get_name():
                return True
        return False


    def create_room(self, roomName, client):
        if self.verify_chat_room_duplicate(roomName):
            room = Room(roomName, client.get_socket())
            room.add_member(client.get_socket)
            self.rooms.append(room)
            client.get_socket().send(bytes('Sala creada exitosamente',
                                            'UTF-8'))
        else:
            client.get_socket().send(bytes('Ya existe una sala con ese nombre',
                                            'UTF-8'))


    def get_people_invited(self, users):
        invited = []
        for user in users:
            if Room.verify_if_is_invited(user):
                invited.append(user)
        return invited


    def get_unique_users(self, users):
        users_without_duplicates = []
        for user in range(2, len(users)):
            if users[user] not in users_without_duplicates:
                users_without_duplicates.append(users[user])
        return users_without_duplicates


    def invite_users(self, roomName, users, client):
        for room in self.rooms:
            if room.get_name() == roomName:
                if room.verify_owner(client.get_socket()):
                    for user in users:
                        room.invite_member(user)
                        user.send(bytes('Has sido invidado a la sala {} por'
                                        'parte de {}'.format(roomName, client.get_name()),
                                        'UTF-8'))
                    Client.get_socket().send(bytes('Todos han sido invitados',
                                                   'UTF-8'))

                else:
                    client.get_socket().send(bytes('No eres el dueño de la sala',
                                                   'UTF-8'))












    def receive_message(self, client):
        while True:
            message = client.get_socket().recv(1024)
            message = message.decode('utf-8')
            message = message.split(' ')

            if message[0] == Protocol.IDENTIFY.value:
                if len(message) > 1:
                    self.change_client_name(message[1], client)
                else:
                    client.get_socket().send(bytes('No se especifico nombre',
                                                   'UTF-8'))


            elif message[0] == Protocol.STATUS.value:
                if len(message) > 1:
                    self.change_user_status(message[1], client)
                else:
                    client.get_socket().send(bytes('No se especifico status',
                                                   'UTF-8'))


            elif message[0] == Protocol.MESSAGE.value:
                if len(message) > 2:
                    message_to_user = message[1]
                    userMessage = self.get_user_message(message, 2)
                    self.send_direct_message(message_to_user, userMessage, client)
                else:
                    if len(message == 1):
                        client.get_socket().send(bytes('No se especifico'
                                                       'mensaje', 'UTF-8'))
                    else:
                        client.get_socket().send(bytes('No se especifico'
                                                       'usuario ni mensaje',
                                                       'UTF-8'))


            elif message[0] == Protocol.USERS.value:
                self.send_clients()


            elif message[0] == Protocol.PUBLICMESSAGE.value:
                if len(message) > 1:
                    userMessage = self.get_user_message(message, 1)
                    self.send_public_message(userMessage)
                else:
                    client.get_socket().send(bytes('No se especifico mensaje',
                                                   'UTF-8'))


            elif message[0] == Protocol.CREATEROOM.value:
                if len(message) > 1:
                    roomName = message[1]
                    self.create_room(roomName, client)
                else:
                    client.get_socket().send(bytes('No se especifico nombre'
                                                   'de la sala', 'UTF-8'))


            elif message[0] == Protocol.INVITE.value:
                roomName = message[0]
                if len(message) > 2 and self.verify_chat_room_existance(roomName):
                    users_verified = self.get_unique_users(message)
                    sockets = self.get_sockets(users_verified)
                    self.invite_users(roomName, sockets, client)
                else:
                    if self.verify_chat_room_existance(roomName) == False:
                        client.get_socket().send(bytes('No existe una sala'
                                                        'con ese nombre',
                                                        'UTF-8'))
                    elif len(message == 1):
                        client.get_socket().send(bytes('No se especificaron'
                                                       'los invitados a la'
                                                       'sala', 'UTF-8'))
                    else:
                        client.get_socket().send(bytes('No se especifico el'
                                                       'nombre de la sala ni'
                                                       'los invitados',
                                                       'UTF-8'))


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
