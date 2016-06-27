import socket

import config


class Connection:
    def __init__(self, **kwargs):
        print("Creating new IRC connection with the following configuration:")
        print("nick: " + config.get('nick'))
        print("server: " + config.get('server'))

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((config.get('server'), config.get('port')))

    def join_channel(self, channel):
        self.sock.send("JOIN " + channel)
