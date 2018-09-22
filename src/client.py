import sys
from src.status import Status

"""estructura del cliente"""
class Client:
    def __init__(self, name, socket, ip):
        """constructor que inicaliza nombre, socket e ip"""
        self.name = ''
        self.status = Status.ACTIVE.value
        self.socket = socket
        self.ip = ip

    def set_name(self, name):
        """asigna el nombre"""
        self.name = name

    def has_name(self, user):
        """verifica si el usuario tiene nombre"""
        return user.get_name() != ''

    def get_name(self):
        """regresa el nombre"""
        return self.name

    def set_status(self, status):
        """asigna estado"""
        self.status = status

    def get_status(self):
        """regresa estado"""
        return self.status

    def set_socket(self, socket):
        """asigna socket"""
        self.socket = socket

    def get_socket(self):
        """regresa socket"""
        return self.socket

    def set_ip(self, ip):
        """asigna ip"""
        self.ip = ip

    def get_ip(self):
        """regresa ip"""
        return self.ip

    def __str__(self):
        """regresa cadena del nombre"""
        return self.name
