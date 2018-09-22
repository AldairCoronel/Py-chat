import sys
from enum import Enum

"""enumeracion del protocolo"""
class Protocol(Enum):

    IDENTIFY = 'IDENTIFY'

    STATUS = 'STATUS'

    USERS = 'USERS'

    MESSAGE = 'MESSAGE'

    PUBLICMESSAGE = 'PUBLICMESSAGE'

    CREATEROOM = 'CREATEROOM'

    INVITE = 'INVITE'

    JOINROOM = 'JOINROOM'

    ROOMMESSAGE = 'ROOMMESSAGE'

    DISCONNECT = 'DISCONNECT'
