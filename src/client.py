import sys
from src.status import Status

class Client:
    def __init__(self, name, socket, ip):
        self.name = ''
        self.status = Status.ACTIVE.value
        self.socket = socket
        self.ip = ip

    def set_name(self, name):
        self.name = name

    def has_name(self, user):
        return user.get_name() != ''

    def get_name(self):
        return self.name

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def set_socket(self, socket):
        self.socket = socket

    def get_socket(self):
        return self.socket

    def set_ip(self, ip):
        self.ip = ip

    def get_ip(self):
        return self.ip

    def __str__(self):
        return self.name
