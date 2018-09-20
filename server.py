import sys
from src.server import Server  

if len(sys.argv) != 2:
    print ("Error: necesitas pasar: archivo, puerto.")
    exit()
PORT = int(sys.argv[1])
server = Server(PORT)
server.arriba()
