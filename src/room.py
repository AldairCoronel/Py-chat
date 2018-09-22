import sys
from src import *

"""clase sala"""
class Room:

    def __init__(self, name, owner):
        """constructor que inicaliza listas, nombre y dueño"""
        self.name = name
        self.owner = owner
        self.members = []
        self.peopleInvited = []

    def get_name(self):
        """regresa el nombre de la sala"""
        return self.name

    def invite_member(self, user):
        """invita a alguien"""
        self.peopleInvited.append(user)

    def add_member(self, user):
        """añade a un miembro"""
        self.members.append(user)

    def get_members(self):
        """regresa miembros"""
        return self.members

    def get_owner(self):
        """regresa el dueño de la sala"""
        return self.owner

    def delete_client_from_invited(self, user):
        """elimina a usuario de la lista de invitados"""
        for person in self.peopleInvited:
            if person == user.get_socket():
                self.peopleInvited.remove(person)

    def delete_client_from_members(self, user):
        """elimina a usuario de la lista de miembros"""
        for member in self.members:
            if member == user.get_socket():
                self.members.remove(member)

    def verify_owner(self, user):
        """verifica que el usuario sea el dueño"""
        return self.owner == user

    def verify_if_is_invited(self, user):
        """verifica si el usuario esta invitado"""
        for person in self.peopleInvited:
            if person == user:
                return True
        return False

    def verify_if_is_member(self, user):
        """verifica si el usuario es miembro"""
        for member in self.members:
            if user == member:
                return True
        return False
