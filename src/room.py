import sys
from src import *

class Room:

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.members = []
        self.peopleInvited = []

    def get_name(self):
        return self.name

    def invite_member(self, user):
        userSocket = user.get_socket()
        self.peopleInvited.append(userSocket)

    def add_member(self, user):
        self.members.append(user)

    def get_members(self):
        return self.members

    def get_owner(self):
        return self.owner

    
