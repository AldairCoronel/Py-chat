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
        self.peopleInvited.append(user)

    def add_member(self, user):
        self.members.append(user)

    def get_members(self):
        return self.members

    def get_owner(self):
        return self.owner

    def verify_owner(self, user):
        return self.owner == user

    def verify_if_is_invited(self, user):
        for person in self.peopleInvited:
            if person == user:
                return True
        return False
