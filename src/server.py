import sys, socket, threading
from src.protocol import Protocol
from src.client import Client
from src.status import Status
from src.room import Room

"""Clase servidor"""
class Server:
    clients = []
    rooms = []
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    aceptarClientes = False


    def __init__(self, PORT):
        """constructor que inicaliza las listas, puerto, ip"""
        self.server.bind(('0.0.0.0', PORT))
        self.server.listen(10000)
        self.clients = []
        self.rooms = []
        self.aceptarClientes = True


    def name_is_unique(self, name):
        """recibe un nombre y regresa si es el unico en la lista de usuarios"""
        unique = True
        for client in self.clients:
            unique = unique and (False if name == client.get_name() else True)
        return unique


    def change_client_name(self, name, client):
        """recibe nombre y cliente y cambia el nombre del cliente"""
        if self.name_is_unique(name):
            client.set_name(name)
            self.send_message('Usuario actualizado exitosamente.', client.get_socket())
        else:
            self.send_message('Nombre repetido.', client.get_socket())


    def send_clients(self, client):
        """recibe cliente y envia usuarios registrados"""
        listClients = 'Clientes registrados: '
        listClients += ','.join(map(str, self.clients))
        for client in self.clients:
            self.send_message(listClients, client.get_socket())


    def verify_user_existance(self, user):
        """recibe un usuario y regresa si esta en la lista de clientes"""
        for client in self.clients:
            if user == client.get_name():
                return True
        return False


    def get_user_socket(self, user):
        """recibe un usuerio y regresa su socket"""
        for client in self.clients:
            if user == client.get_name():
                return client.get_socket()


    def send_public_message(self, userMessage):
        """recibe un mensaje y lo envia a todos los usuarios"""
        for client in self.clients:
            self.send_message(userMessage, client.get_socket())


    def send_direct_message(self, user, message, client):
        """recibe usuario, mensaje, cliente y envia el mensaje al usuario"""
        if self.verify_user_existance(user):
            destination = self.get_user_socket(user)
            self.send_message(message, destination)
        else:
            self.send_message('Usuario no encontrado.', client.get_socket())


    def send_room_message(self, room, roomMessage):
        """recibe sala, mensaje y envia el mensaje a la sala"""
        members = room.get_members()
        for member in members:
            member.send(bytes(roomMessage, 'UTF-8'))


    def verify_status(self, status, client):
        """recibe estado, cliente y verifica si es valido"""
        verified = True
        if status == client.get_status():
            self.send_message('Estado enviado es igual a tu estado actual.',
                               client.get_socket())
            verified = False
        elif status != Status.ACTIVE.value and \
             status != Status.AWAY.value and \
             status != Status.BUSY.value:
            self.send_message('Manda un estado valido: ACTIVE, AWAY o BUSY',
                               client.get_socket())
            verified = False
        return verified


    def change_user_status(self, status, client):
        """recibe estado, ciente y cambia el estado del cliente"""
        if self.verify_status(status, client):
            client.set_status(status)
            self.send_message('Estado actualizado exitosamente.', client.get_socket())


    def get_user_message(self, message, index):
        """recibe lista de mensajes e indice y regresa el mensaje concatenado"""
        userMessage = ''
        for i in range(index, len(message)):
            userMessage += message[i] + ' '
        return userMessage


    def get_sockets(self, users):
        """recibe usuarios y regresa sockets"""
        sockets = []
        for user in users:
            for client in self.clients:
                if user == client.get_name():
                    sockets.append(client.get_socket())
        return sockets


    def verify_chat_room_duplicate(self, roomName):
        """recibe nombre de sala y verifica si no es un nombre duplicado"""
        for room in self.rooms:
            if roomName == room.get_name():
                return False
        return True

    def verify_chat_room_existance(self, roomName):
        """recibe nombre de sala y verifica si existe"""
        for room in self.rooms:
            if room.get_name() == roomName:
                return True
        return False


    def create_room(self, roomName, client):
        """recibe nombre de sala, cliente y crea una sala"""
        if self.verify_chat_room_duplicate(roomName):
            room = Room(roomName, client.get_socket())
            room.add_member(client.get_socket())
            self.rooms.append(room)
            self.send_message('Sala creada exitosamente.', client.get_socket())
        else:
            self.send_message('Ya existe una sala con ese nombre.', client.get_socket())


    def get_people_invited(self, users):
        """recibe usuarios y regresa a los usuarios invitados"""
        invited = []
        for user in users:
            if Room.verify_if_is_invited(user):
                invited.append(user)
        return invited


    def get_unique_users(self, users):
        """recibe usuarios y regresa usuarios sin duplicados"""
        users_without_duplicates = []
        for user in range(2, len(users)):
            if users[user] not in users_without_duplicates:
                users_without_duplicates.append(users[user])
        return users_without_duplicates


    def invite_users(self, roomName, users, client):
        """recibe nombre de sala, usuarios, cliente e invita los usuarios a la sala"""
        for room in self.rooms:
            if room.get_name() == roomName:
                if room.verify_owner(client.get_socket()):
                    for user in users:
                        room.invite_member(user)
                        if client.has_name(client):
                            name = client.get_name()
                        else:
                            name = client.get_ip()
                        self.send_message('Has sido invidado a la sala {} por '
                                        'parte de {}.'.format(roomName, name), user)
                    self.send_message('Todos han sido invitados.', client.get_socket())
                else:
                    self.send_message('No eres dueno de la sala.', client.get_socket())


    def join_room(self, client, room):
        """recibe cliente, sala y mete al cliente a la sala"""
        if room.verify_if_is_invited(client):
            room.add_member(client)
            self.send_message('Te has unido a la sala {}'.format(room.get_name()), client)
        else:
            self.send_message('No estas invitado a la sala.', client)


    def get_room(self, roomName):
        """recibe nombre de sala y regresa el objeto sala"""
        for room in self.rooms:
            if roomName == room.get_name():
                return room


    def send_message(self, message, socket):
        """recibe mensaje, socket y lo envia a ese cliente"""
        socket.send(bytes(message, 'UTF-8'))


    def delete_client(self, client):
        """recibe cliente y lo elimina de la lista de clientes"""
        for c in self.clients:
            if client == c:
                self.clients.remove(c)


    def kill_client(self, client):
        """recibe cliente y lo mata"""
        self.delete_client(client)
        for room in self.rooms:
            room.delete_client_from_invited(client)
            room.delete_client_from_members(client)


    def receive_message(self, client):
        """recibe cliente y escucha lo que manda"""
        connected = True
        while connected:
            message = client.get_socket().recv(1024)
            message = message.decode('UTF-8')
            message = message.split(' ')

            if message[0] == Protocol.IDENTIFY.value:
                if len(message) > 1:
                    self.change_client_name(message[1], client)
                else:
                    self.send_message('No se especifico nombre.', client.get_socket())


            elif message[0] == Protocol.STATUS.value:
                if len(message) > 1:
                    self.change_user_status(message[1], client)
                else:
                    self.send_message('No se especifico status.', client.get_socket())


            elif message[0] == Protocol.MESSAGE.value:
                if len(message) > 2:
                    message_to_user = message[1]
                    userMessage = self.get_user_message(message, 2)
                    self.send_direct_message(message_to_user, userMessage, client)
                else:
                    if len(message == 1):
                        self.send_message('No se especifico mensaje.', client.get_socket())
                    else:
                        self.send_message('No se especifico usuario ni mensaje.',
                                           client.get_socket())


            elif message[0] == Protocol.USERS.value:
                self.send_clients(client)


            elif message[0] == Protocol.PUBLICMESSAGE.value:
                if len(message) > 1:
                    userMessage = self.get_user_message(message, 1)
                    self.send_public_message(userMessage)
                else:
                    self.send_message('No se especifico mensaje.', client.get_socket())


            elif message[0] == Protocol.CREATEROOM.value:
                if len(message) > 1:
                    roomName = message[1]
                    self.create_room(roomName, client)
                else:
                    self.send_message('No se especifico nombre de la sala.', client.get_socket())


            elif message[0] == Protocol.INVITE.value:
                if len(message) > 2 and self.verify_chat_room_existance(roomName):
                    roomName = message[1]
                    users_verified = self.get_unique_users(message)
                    sockets = self.get_sockets(users_verified)
                    if len(sockets) > 0:
                        self.invite_users(roomName, sockets, client)
                    else:
                        self.send_message('No existen los usuarios que quieres invitar.',
                                           client.get_socket())
                else:
                    if len(message) == 2:
                        self.send_message('No se especificaron los invitados a la sala.',
                                           client.get_socket())
                    elif len(message) == 1:
                        self.send_message('No se especifico el nombre de la sala ni los invitados.',
                                           client.get_socket())
                    elif self.verify_chat_room_existance(roomName) == False:
                        self.send_message('No existe una sala con ese nombre.',
                                           client.get_socket())


            elif message[0] == Protocol.JOINROOM.value:
                if len(message) > 1:
                    roomName = message[1]
                    if self.verify_chat_room_existance(roomName):
                        room = self.get_room(roomName)
                        self.join_room(client.get_socket(), room)
                    else:
                        self.send_message('La sala no existe.', client.get_socket())
                else:
                    self.send_message('No se especifico la sala.', client.get_socket())


            elif message[0] == Protocol.ROOMMESSAGE.value:
                if len(message) > 2:
                    roomName = message[1]
                    if self.verify_chat_room_existance(roomName):
                        room = self.get_room(roomName)
                        roomMessage = self.get_user_message(message, 2)
                        self.send_room_message(room, roomMessage)
                    else:
                        self.send_message('La sala no existe.', client.get_socket())
                else:
                    if len(message) == 1:
                        self.send_message('No se especifico el nombre de la sala ni el mensaje.',
                                           client.get_socket())
                    else:
                        self.send_message('No se especifico el mensaje.', client.get_socket())

            elif message[0] == Protocol.DISCONNECT.value:
                if len(message) == 1:
                    self.send_message('Bye bye', client.get_socket())
                    self.kill_client(client)
                    client.get_socket().close()
                    connected = False
                else:
                    self.send_message('Solo debes mandar DISCONNECT', client.get_socket())


            else:
                msg = ''
                msg += 'Mensaje invalido. A continuacion tiene la lista de mensajes validos: '
                msg += '| IDENTIFY nombre : para identificar usuario'
                msg += '| STATUS status: asigna estado al usuario: ACTIVE, BUSY o AWAY'
                msg += '| USERS: muestra los usuarios identificados'
                msg += '| MESSAGE usuario mensaje: envia mensaje privado al usuario'
                msg += '| PUBLICMESSAGE mensaje: envia el mensaje a todos los usuarios identificados'
                msg += '| CREATEROOM nombre: crea una sala con ese nombre, siendo el dueno el usario que la creo'
                msg += '| INVITE nombre usuario1 usuario2...: envia invitaciones a los usuarios para unirse a la sala'
                msg += '| JOINROOM nombre: acepta la invitacion a la sala que fuiste invitado'
                msg += '| ROOMMESSAGE nombre mensaje: envia mensaje a los usuarios de la sala'
                msg += '| DISCONNECT: te desconectas del servidor'
                self.send_message(msg, client.get_socket())

            if not message:
                break


    def arriba(self):
        """sube el servidor"""
        while self.aceptarClientes:
                connection, address = self.server.accept()
                client = Client(None, connection, address)
                print('Acaba de conectarse ', address)
                self.clients.append(client)
                serverThread = threading.Thread(target = self.receive_message,
                                args=(client,))
                serverThread.start()
