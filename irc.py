import socket
import time

import config

BUFSIZE = 512

class Connection:
    def __init__(self, **kwargs):
        print("Creating new IRC connection with the following configuration:")
        print(open('config.yaml', 'r').read())

        self.connect()

        for channel in config.get('channels'):
            self.connection.join_channel(channel)

        while True:
            message = self.connection.sock.recv(BUFSIZE)
            if message:
                self.parse_message(message)

    def parse_message(self, message):
        messages = message.split("\r\n")

        for msg in messages:
            if msg:
                print(" [RECV] <-- " + repr(m))

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((config.get('server'), config.get('port')))
        time.sleep(1)

    def join_channel(self, channel):
        print("Joining channel: " + channel)
        self.send_message("JOIN " + channel)

    def send_message(self, message):
        print(" [SEND] --> " + repr(message))
        self.sock.send(message + "\r\n")
