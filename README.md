# Chat

Chat using MVC for MyP class.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites


```
Python 3.7 is required to run this project
```

### Installing

First clone this project

```
git clone https://github.com/AldairCoronel/chat.git
```
Go to
```
cd chat/
```
To run the server

```
python3 server.py 1234
```

Open one more terminal and run the client

```
python3 client.py localhost 1234
```

then you can simply play with it

PROTOCOL

```
• IDENTIFY username
```
Este comando identifica al usuario, username será el nombre del usuario, ejemplo: IDENTIFY Kimberly
```
• STATUS userstatus
```
Este comando asignará el estado al usuario, userstatus es uno de los tres posibles estados, ejemplo: STATUS
AWAY
```
• USERS
```
Mostrará los usuarios identificados, ejemplo: USERS
```
• MESSAGE username messageContent
```
Enviará un mensaje privado a username, y el mensaje será messageContent, ejemplo: MESSAGE Luis Hola
Luis
```
• PUBLICMESSAGE messageContent
```
Enviará el mensaje a todos los usuarios identificados, ejemplo: PUBLICMESSAGE Hola a todos!
```
• CREATEROOM roomname
```
Se creará una sala en el servidor con nombre roomname y el dueño de la sala será el que la creó, ejemplo:
CREATEROOM SALA1
```
• INVITE roomname username1 username2,...
```
Enviará una invitación a la lista de usuarios para unirse a la sala roomname, ejemplo: INVITE SALA1 LUIS
KIM FER
```
• JOINROOM roomname
```
Aceptará la invitación a la sala roomname que fue invitado, JOINROOM SALA1
```
• ROOMESSAGE roomname messageContent
```
Enviará el mensaje a todos los usuarios dentro de esa sala, ejemplo: ROOMESSAGE sala1 Hola sala1!

```
• DISCONNECT
```
El usuario se desconecta del servidor, ejemplo: DISCONNECT




## Authors

* **Aldair Coronel Ruiz**
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


