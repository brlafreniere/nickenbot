import socket

import config

BUFSIZE = 512

class Connection:
    def __init__(self, **kwargs):
        print("Creating new IRC connection with the following configuration:")
        print("nick: " + config.get('nick'))
        print("server: " + config.get('server'))

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((config.get('server'), config.get('port')))

    def recv_message(self):
        print(self.sock.recv(BUFSIZE))
