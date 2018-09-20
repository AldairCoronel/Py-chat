import sys


class Client:
    def __init__(name, socket, ip):
        self.name = ''
        self.status = True
        self.socket = socket
        self.ip = ip

    def set_name(name):
        self.name = name

    def get_name():
        return self.name

    def set_status(status):
        self.status = status

    def get_status():
        return self.status

    def set_socket(socket):
        self.socket = socket

    def get_socket():
        return self.socket

    def set_ip(ip):
        self.ip = ip

    def get_ip():
        return self.ip
